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

from .helpers import desc, format_address
from ..models import py2html, Code
from ..utils import iterate as h_iterate
from ..catalogs import trans

current_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)

complement_order = {
    "TimbreFiscalDigital": 1
}


def finalize(s):
    if isinstance(s, Decimal):
        return s.__format__(",f")

    if isinstance(s, Undefined):
        return do_mark_safe("&nbsp;")

    return s


class CFDIEnvironment(Environment):
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
        search_path = [os.path.join(current_dir, 'templates')]
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
                meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
                            'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                return meses[m - 1]
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
            if not data:
                return do_mark_safe("&nbsp;")

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

        @self.filter
        def code(s):
            if isinstance(s, Code):
                return s.code
            return s


class PDFFIleSystemLoader(FileSystemLoader):
    def get_source(
            self, environment: Environment, template: str
    ):
        try:
            return super().get_source(environment, template)
        except TemplateNotFound:
            return "{{ c | dump }}", None, lambda: True


DefaultCFDIEnvironment = CFDIEnvironment()
