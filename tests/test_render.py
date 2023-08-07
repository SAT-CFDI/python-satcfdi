import glob
import os

from satcfdi import render
from satcfdi.cfdi import CFDI
from satcfdi.render import BODY_TEMPLATE
from satcfdi.render.environment import CFDIEnvironment
from tests.utils import verify_result

current_dir = os.path.abspath(os.path.dirname(__file__))


def test_single_html_file():
    all_invoices = []
    for f in glob.iglob(os.path.join(current_dir, "invoices", "*.xml")):
        c = CFDI.from_file(f)
        all_invoices.append(c)

    res = render.html_str(all_invoices)
    verify_result(res, "multiple_invoices.html")

    render.html_write(
        xlm=all_invoices,
        target=os.path.join(current_dir, "test_render", "multiple_invoices2.html"),
    )

    with open(os.path.join(current_dir, "test_render", "multiple_invoices2.html"), "r", encoding='utf-8') as f:
        assert f.read() == res

    # assert filecmp.cmp(
    #     os.path.join(current_dir, "test_accounting", "multiple_invoices.html"),
    #     os.path.join(current_dir, "test_accounting", "multiple_invoices2.html")
    # )


def verify_custom_template(invoice, path):
    template_env = CFDIEnvironment(
        templates_path=os.path.join(current_dir, 'templates')
    )

    verify = verify_result(
        data=render.html_str(invoice, template=template_env.get_template("_main.html")),
        filename=f"{path}.html"
    )
    assert verify


def test_custom_template():
    xml_file = "cfdv40-ejemplo.xml"
    cfdi = CFDI.from_file(
        os.path.join(current_dir, 'cfdi_ejemplos/comprobante40', xml_file)
    )

    verify_custom_template(cfdi, xml_file)


def test_body_html():
    xml_file = "cfdv40-ejemplo.xml"
    cfdi = CFDI.from_file(
        os.path.join(current_dir, 'cfdi_ejemplos/comprobante40', xml_file)
    )

    body_html = render.html_str(cfdi, template=BODY_TEMPLATE)

    verify = verify_result(
        data=body_html,
        filename=f"{xml_file}.body.html"
    )
    assert verify


