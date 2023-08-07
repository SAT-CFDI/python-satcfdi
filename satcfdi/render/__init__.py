import json
from collections.abc import Sequence
from lxml.etree import QName

from .environment import DefaultCFDIEnvironment
from ..xelement import XElement

try:
    import weasyprint

    PDF_CSS = weasyprint.CSS(string="@page {margin: 1.0cm 1.27cm 1.1cm 0.85cm;}")
except OSError as ex:
    weasyprint = None

MAIN_TEMPLATE = DefaultCFDIEnvironment.get_template("_main.html")
BODY_TEMPLATE = DefaultCFDIEnvironment.get_template("_body.html")


def json_write(xlm: XElement, target, pretty_print=False):
    if isinstance(target, str):
        with open(target, 'w') as f:
            json.dump(xlm, f, ensure_ascii=False, default=str, indent=2 if pretty_print else None)
            return

    json.dump(xlm, target, ensure_ascii=False, default=str, indent=2 if pretty_print else None)


def json_str(xlm: XElement, pretty_print=False) -> str:
    return json.dumps(xlm, ensure_ascii=False, default=str, indent=2 if pretty_print else None)


def html_write(xlm: XElement | Sequence[XElement], target, template=MAIN_TEMPLATE):
    if isinstance(xlm, Sequence):
        template.stream({"c": [(QName(a.tag).localname, a) for a in xlm], "k": '_multiple'}).dump(target)
    else:
        template.stream({"c": xlm, "k": QName(xlm.tag).localname}).dump(target)


def html_str(xlm: XElement | Sequence[XElement], template=MAIN_TEMPLATE) -> str:
    if isinstance(xlm, Sequence):
        return template.render({"c": [(QName(a.tag).localname, a) for a in xlm], "k": '_multiple'})
    else:
        return template.render({"c": xlm, "k": QName(xlm.tag).localname})


def pdf_write(xlm: XElement | Sequence[XElement], target, template=MAIN_TEMPLATE):
    if weasyprint is None:
        raise ImportError("weasyprint is not installed")

    weasyprint.HTML(string=html_str(xlm, template=template)).write_pdf(
        target=target,
        stylesheets=[PDF_CSS]
    )


def pdf_bytes(xlm: XElement | Sequence[XElement], template=MAIN_TEMPLATE) -> bytes:
    if weasyprint is None:
        raise ImportError("weasyprint is not installed")

    return weasyprint.HTML(string=html_str(xlm, template=template)).write_pdf(
        stylesheets=[PDF_CSS]
    )
