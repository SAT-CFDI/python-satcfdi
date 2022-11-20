import base64
import logging
import os
from decimal import Decimal
from html import escape as html_escape
from io import BytesIO

import qrcode
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from jinja2.filters import do_mark_safe
from jinja2.runtime import Undefined
from lxml.etree import QName

# noinspection PyUnresolvedReferences
from .catalog import CATALOGS
from .helpers import desc, format_address, trans, iterate as h_iterate
from ..models import py2html

current_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)

complement_order = {
    "TimbreFiscalDigital": 1
}


def finalize(s):
    if isinstance(s, Decimal):
        # format Decimal with at least 2 decimal places and coma separated
        full_number = "{:0,}".format(s)
        if "." in full_number:
            full_number = full_number.rstrip("0")
        return max("{:0,.2f}".format(s), full_number, key=len)

    if isinstance(s, Undefined):
        return do_mark_safe("&nbsp;")

    return s


class PDFEnvironment(Environment):
    @property
    def filter(self):
        def sub(f):
            self.filters[f.__name__] = f
            return f

        return sub

    @property
    def glob(self):
        def sub(f):
            self.globals[f.__name__] = f
            return f

        return sub

    def __init__(self, templates_path=None):
        search_path = [os.path.join(current_dir, 'pdf_templates')]
        if templates_path:
            search_path.insert(0, templates_path)

        super().__init__(
            loader=PDFFIleSystemLoader(searchpath=search_path),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )

        self.filters['desc'] = desc
        self.filters['trans'] = trans
        self.finalize = finalize

        @self.glob
        def iterate(v):
            if isinstance(v, Undefined):
                return v
            return h_iterate(v)

        @self.filter
        def qr_image(url):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=5,
                border=0,
            )
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            with BytesIO() as buffered:
                img.save(buffered, format="PNG")
                return base64.b64encode(buffered.getvalue()).decode("utf-8")

        @self.filter
        def mes(m):
            if isinstance(m, int):
                m = "{:0>2}".format(m)
                return CATALOGS['{http://www.sat.gob.mx/esquemas/retencionpago/1/catalogos}c_Periodo'][m]
            return m

        @self.glob
        def iterate_complements(items):
            def sort_order(x):
                return complement_order.get(QName(x.tag).localname, 0)

            return [(QName(x.tag).localname, x) for x in sorted(iterate(items), key=sort_order)]

        @self.glob
        def tasa_cuota(factor, s):
            if factor == "Tasa":
                return "{:%}".format(s)
            return s

        @self.filter
        def address(k):
            if k:
                address = format_address(k)
                return do_mark_safe(
                    html_escape(address).replace('\n', '<br>')
                )
            return k

        @self.filter
        def dump(data):
            if data:
                res = py2html.dumps(data, escape=True, clubbing=True, translate_keys=trans, default=finalize)
                return do_mark_safe(res)
            return data

        @self.filter
        def simple(data, *args):
            def fields():
                for k in args or data.keys():
                    if v := data.get(k):
                        yield f"<div><b>{html_escape(trans(k))}: </b>{dump(v)}</div>"

            return do_mark_safe(
                "".join(fields())
            )

        @self.filter
        def baa(s):
            r = "&#8203;".join(html_escape(str(s)))
            return do_mark_safe(r)


class PDFFIleSystemLoader(FileSystemLoader):
    def get_source(
            self, environment: Environment, template: str
    ):
        try:
            return super().get_source(environment, template)
        except TemplateNotFound:
            return "{{ c | dump }}", None, lambda: True


DefaultPDFEnvironment = PDFEnvironment()
