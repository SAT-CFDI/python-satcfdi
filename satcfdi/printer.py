from lxml.etree import QName

try:
    import weasyprint
    PDF_CSS = weasyprint.CSS(string="@page {margin: 1.0cm 1.27cm 1.1cm 0.85cm;}")
except OSError as ex:
    weasyprint = None

from .render import PDF_INIT_TEMPLATE


class Representable:
    tag = None

    def html_write(self, target, init_template=PDF_INIT_TEMPLATE):
        init_template.stream({"c": self, "k": QName(self.tag).localname}).dump(target)

    def html_str(self, init_template=PDF_INIT_TEMPLATE) -> str:
        return init_template.render({"c": self, "k": QName(self.tag).localname})

    def pdf_write(self, target, init_template=PDF_INIT_TEMPLATE):
        if weasyprint is None:
            raise ImportError("weasyprint is not installed")

        weasyprint.HTML(string=self.html_str(init_template=init_template)).write_pdf(
            target=target,
            stylesheets=[PDF_CSS]
        )

    def pdf_bytes(self, init_template=PDF_INIT_TEMPLATE) -> bytes:
        if weasyprint is None:
            raise ImportError("weasyprint is not installed")

        return weasyprint.HTML(string=self.html_str(init_template=init_template)).write_pdf(
            stylesheets=[PDF_CSS]
        )

    @staticmethod
    def html_write_all(objs, target, init_template=PDF_INIT_TEMPLATE):
        init_template.stream({"c": [(QName(a.tag).localname, a) for a in objs], "k": '_multiple'}).dump(target)

    @staticmethod
    def html_str_all(objs, init_template=PDF_INIT_TEMPLATE) -> str:
        return init_template.render({"c": [(QName(a.tag).localname, a) for a in objs], "k": '_multiple'})

    @staticmethod
    def pdf_write_all(objs, target, init_template=PDF_INIT_TEMPLATE):
        if weasyprint is None:
            raise ImportError("weasyprint is not installed")

        weasyprint.HTML(string=Representable.html_str_all(objs, init_template=init_template)).write_pdf(
            target=target,
            stylesheets=[PDF_CSS]
        )

    @staticmethod
    def pdf_bytes_all(objs, init_template=PDF_INIT_TEMPLATE) -> bytes:
        if weasyprint is None:
            raise ImportError("weasyprint is not installed")

        return weasyprint.HTML(string=Representable.html_str_all(objs, init_template=init_template)).write_pdf(
            stylesheets=[PDF_CSS]
        )
