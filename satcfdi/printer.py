from lxml.etree import QName

try:
    import weasyprint
    PDF_CSS = weasyprint.CSS(string="@page {margin: 1.0cm 1.27cm 1.1cm 0.85cm;}")
except OSError as ex:
    weasyprint = None

from .render import PDF_INIT_TEMPLATE
from .render.environment import CFDIEnvironment


class Representable:
    tag = None

    def html_write(self, target, templates_path=None):
        if templates_path:
            env = CFDIEnvironment(templates_path=templates_path)
            init_template = env.get_template("_init.html")
        else:
            init_template = PDF_INIT_TEMPLATE

        init_template.stream({"c": self, "k": QName(self.tag).localname}).dump(target)

    def html_str(self, templates_path=None) -> str:
        if templates_path:
            env = CFDIEnvironment(templates_path=templates_path)
            init_template = env.get_template("_init.html")
        else:
            init_template = PDF_INIT_TEMPLATE

        return init_template.render({"c": self, "k": QName(self.tag).localname})

    def pdf_write(self, target, templates_path=None):
        if weasyprint is None:
            raise ImportError("weasyprint is not installed")

        weasyprint.HTML(string=self.html_str(templates_path=templates_path)).write_pdf(
            target=target,
            stylesheets=[PDF_CSS]
        )

    def pdf_bytes(self, templates_path=None) -> bytes:
        if weasyprint is None:
            raise ImportError("weasyprint is not installed")

        return weasyprint.HTML(string=self.html_str(templates_path=templates_path)).write_pdf(
            stylesheets=[PDF_CSS]
        )

    @staticmethod
    def html_write_all(objs, target, templates_path=None):
        if templates_path:
            env = CFDIEnvironment(templates_path=templates_path)
            init_template = env.get_template("_multiple.html")
        else:
            init_template = PDF_INIT_TEMPLATE

        init_template.stream({"c": [(QName(a.tag).localname, a) for a in objs], "k": '_multiple'}).dump(target)

    @staticmethod
    def html_str_all(objs, templates_path=None) -> str:
        if templates_path:
            env = CFDIEnvironment(templates_path=templates_path)
            init_template = env.get_template("_multiple.html")
        else:
            init_template = PDF_INIT_TEMPLATE

        return init_template.render({"c": [(QName(a.tag).localname, a) for a in objs], "k": '_multiple'})
