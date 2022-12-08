from lxml.etree import QName
from weasyprint import HTML, CSS

from .transform import *
from .transform.pdf_environment import PDFEnvironment

PDF_CSS = CSS(string="@page {margin: 1.0cm 1.27cm 1.1cm 0.85cm;}")


class Representable:
    def html_write(self, target, templates_path=None):
        if templates_path:
            env = PDFEnvironment(templates_path=templates_path)
            init_template = env.get_template("_init.html")
        else:
            init_template = PDF_INIT_TEMPLATE

        init_template.stream({"c": self, "k": QName(self.tag).localname}).dump(target)

    def html_str(self, templates_path=None) -> str:
        if templates_path:
            env = PDFEnvironment(templates_path=templates_path)
            init_template = env.get_template("_init.html")
        else:
            init_template = PDF_INIT_TEMPLATE

        return init_template.render({"c": self, "k": QName(self.tag).localname})

    def pdf_write(self, target, templates_path=None):
        HTML(string=self.html_str(templates_path=templates_path)).write_pdf(
            target=target,
            stylesheets=[PDF_CSS]
        )

    def pdf_bytes(self, templates_path=None) -> bytes:
        return HTML(string=self.html_str(templates_path=templates_path)).write_pdf(
            stylesheets=[PDF_CSS]
        )
