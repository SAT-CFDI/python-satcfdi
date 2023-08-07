from collections.abc import Sequence
from lxml.etree import QName

from .environment import DefaultCFDIEnvironment
from ..xelement import XElement

try:
    import weasyprint

    PDF_CSS = weasyprint.CSS(string="@page {margin: 1.0cm 1.27cm 1.1cm 0.85cm;}")
except OSError as ex:
    weasyprint = None

PDF_INIT_TEMPLATE = DefaultCFDIEnvironment.get_template("_init.html")


def html_write(xlm: XElement | Sequence[XElement], target, init_template=PDF_INIT_TEMPLATE):
    if isinstance(xlm, Sequence):
        init_template.stream({"c": [(QName(a.tag).localname, a) for a in xlm], "k": '_multiple'}).dump(target)
    else:
        init_template.stream({"c": xlm, "k": QName(xlm.tag).localname}).dump(target)


def html_str(xlm: XElement | Sequence[XElement], init_template=PDF_INIT_TEMPLATE) -> str:
    if isinstance(xlm, Sequence):
        return init_template.render({"c": [(QName(a.tag).localname, a) for a in xlm], "k": '_multiple'})
    else:
        return init_template.render({"c": xlm, "k": QName(xlm.tag).localname})


def pdf_write(xlm: XElement | Sequence[XElement], target, init_template=PDF_INIT_TEMPLATE):
    if weasyprint is None:
        raise ImportError("weasyprint is not installed")

    weasyprint.HTML(string=html_str(xlm, init_template=init_template)).write_pdf(
        target=target,
        stylesheets=[PDF_CSS]
    )


def pdf_bytes(xlm: XElement | Sequence[XElement], init_template=PDF_INIT_TEMPLATE) -> bytes:
    if weasyprint is None:
        raise ImportError("weasyprint is not installed")

    return weasyprint.HTML(string=html_str(xlm, init_template=init_template)).write_pdf(
        stylesheets=[PDF_CSS]
    )
