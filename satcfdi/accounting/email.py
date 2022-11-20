import imaplib
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
import email
import email.utils
import logging

logger = logging.getLogger(__name__)


class EmailManager:
    def __init__(self, stmp_host, stmp_port, imap_host, imap_port, user, password):
        self.receiver = EmailReceiver(
            host=imap_host,
            port=imap_port,
            user=user,
            password=password
        )
        self.sender = EmailSender(
            host=stmp_host,
            port=stmp_port,
            user=user,
            password=password
        )


class EmailReceiver:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def __enter__(self):
        self.server = imaplib.IMAP4_SSL(self.host, self.port)
        self.server.login(self.user, password=self.password)

        return self.server

    def __exit__(self, exc_type, exc, exc_tb):
        self.server.close()

    def get_mail_attachments(self, mailbox):
        with self as mail:
            mail.select(
                mailbox=mailbox,
                readonly=False
            )

            typ, data = mail.search(None, 'UnSeen')  # mail.search(None, 'ALL')
            logger.info("%s %s", typ, data)

            for num in data[0].split():
                typ, data = mail.fetch(num, '(RFC822)')
                raw_email = data[0][1]
                # print('Message %s\n%s\n' % (num, raw_email))

                # converts byte literal to string removing b''
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)

                xml_data = None
                pdf_data = None

                for part in email_message.walk():
                    # this part comes from the snipped I don't understand yet...
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue

                    file_name = part.get_filename()

                    if file_name:
                        if file_name.endswith(".xml"):
                            if xml_data:
                                yield xml_data, pdf_data
                                pdf_data = None
                            xml_data = part.get_payload(decode=True)
                        elif file_name.endswith(".pdf"):
                            if pdf_data:
                                yield xml_data, pdf_data
                                xml_data = None
                            pdf_data = part.get_payload(decode=True)

                if xml_data or pdf_data:
                    yield xml_data, pdf_data

                # mail.store(
                #     message_set=num,
                #     command='+FLAGS',
                #     flags='\\Seen'
                # )


class EmailSender:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def __enter__(self):
        self.server = smtplib.SMTP(host=self.host, port=self.port)
        self.server.starttls()  # Puts connection to SMTP server in TLS mode

        self.server.login(
            user=self.user,
            password=self.password
        )
        return self

    # exc_type, exc, exc_tb
    def __exit__(self, exc_type, exc, exc_tb):
        self.server.close()

    def send_email(self, subject: str, to_addrs: list, html: str = None, file_attachments=None):
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = ", ".join(to_addrs)
        msg['Subject'] = subject
        if html:
            msg.attach(MIMEText(html, _subtype='html'))

        for f in file_attachments or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

        self.server.send_message(
            msg=msg
        )
