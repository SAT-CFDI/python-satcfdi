import os

from satcfdi.cfdi import CFDI
from satcfdi.render.environment import CFDIEnvironment
from tests.utils import verify_result

module = 'satcfdi'
current_dir = os.path.dirname(__file__)


def verify_invoice(invoice, path):
    template_env = CFDIEnvironment(
        templates_path=os.path.join(current_dir, 'templates')
    )

    verify = verify_result(
        data=invoice.html_str(
            init_template=template_env.get_template("_init.html"),
        ),
        filename=f"{path}.html"
    )
    assert verify
