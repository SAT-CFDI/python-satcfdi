import os
from types import SimpleNamespace
from unittest import mock

from satcfdi.portal.utils import generate_token, verify_token, action_url, get_form_fields
from satcfdi.portal import SATPortal, SATPortalConstancia
from .utils import get_signer

current_dir = os.path.dirname(__file__)
test_dir = os.path.join(current_dir, 'test_portal')
session_file = os.path.join(test_dir, 'session')


def test_portal_get_token():
    code = 'MjFhYzNkODAtN2MxMC00NGU5LWI5NDYtMThmZWZmMjM5OTQ1'
    signer = get_signer('cacx7605101p8')
    token = generate_token(signer, code=code)

    assert code == verify_token(certificate=signer, token=token)


def test_action_url():
    target_url = action_url(
        action="/nidp/app/login?id=fiel&sid=0&option=credential&sid=0",
        url='https://loginda.siat.sat.gob.mx/nidp/app/login?id=fiel'
    )
    assert target_url == 'https://loginda.siat.sat.gob.mx/nidp/app/login?id=fiel&sid=0&option=credential&sid=0'

    target_url = action_url(
        action=None,
        url='https://loginda.siat.sat.gob.mx/nidp/app/login?id=fiel'
    )
    assert target_url == 'https://loginda.siat.sat.gob.mx/nidp/app/login?id=fiel'

    target_url = action_url(
        action="http://aaaa.bbb",
        url='https://loginda.siat.sat.gob.mx/nidp/app/login?id=fiel'
    )
    assert target_url == "http://aaaa.bbb"


def test_start_session():
    signer = get_signer('cacx7605101p8')
    res = SATPortal(signer)

    try:
        with open(session_file, 'rb') as f:
            res.load_session(f)
        print('Session Loaded')
    except FileNotFoundError:
        print('FileNotFound')

    # res.login()

    os.makedirs(test_dir, exist_ok=True)
    with open(session_file, 'wb') as f:
        res.save_session(f)


CONSULTA_TRAMITE_URL = 'https://rfcampc.siat.sat.gob.mx/PTSC/IdcSiat/autc/ReimpresionTramite/ConsultaTramite.jsf'
CONSULTA_TRAMITE_PAGE = """<html><body>
<form id="formReimpAcuse" name="formReimpAcuse" method="post" action="/PTSC/IdcSiat/autc/ReimpresionTramite/ConsultaTramite.jsf">
  <input type="hidden" name="formReimpAcuse" value="formReimpAcuse" />
  <input type="text" name="formReimpAcuse:tipoTramite_filter" />
  <input type="text" name="formReimpAcuse:tipoTramite_focus" />
  <select name="formReimpAcuse:tipoTramite_input">
    <option value="">Seleccione</option>
    <option value="1">Otro</option>
  </select>
  <input type="text" name="formReimpAcuse:fechaInicio_input" value="" />
  <input type="text" name="formReimpAcuse:fechaFin_input" value="" />
  <input type="text" name="formReimpAcuse:folio" value="" />
  <input type="checkbox" name="formReimpAcuse:unchecked" value="1" />
  <input type="submit" name="formReimpAcuse:j_idt47" value="Buscar" />
  <button id="formReimpAcuse:j_idt50" name="formReimpAcuse:j_idt50"><span>Generar Constancia</span></button>
  <input type="hidden" name="javax.faces.ViewState" value="-123:456" />
</form>
</body></html>"""


def test_get_form_fields():
    res = SimpleNamespace(text=CONSULTA_TRAMITE_PAGE, url=CONSULTA_TRAMITE_URL)

    assert get_form_fields(res) == {
        'formReimpAcuse': 'formReimpAcuse',
        'formReimpAcuse:tipoTramite_filter': '',
        'formReimpAcuse:tipoTramite_focus': '',
        'formReimpAcuse:tipoTramite_input': '',
        'formReimpAcuse:fechaInicio_input': '',
        'formReimpAcuse:fechaFin_input': '',
        'formReimpAcuse:folio': '',
        'javax.faces.ViewState': '-123:456',
    }
    assert get_form_fields(SimpleNamespace(text='<html></html>', url=CONSULTA_TRAMITE_URL)) == {}


def test_generar_constancia_submits_the_page_fields():
    portal = SATPortalConstancia(get_signer('cacx7605101p8'))
    pdf = b'%PDF-1.4'
    get_responses = {
        'https://rfcampc.siat.sat.gob.mx/app/seg/SessionBroker': SimpleNamespace(
            status_code=200, text=CONSULTA_TRAMITE_PAGE, url=CONSULTA_TRAMITE_URL
        ),
        'https://rfcampc.siat.sat.gob.mx/PTSC/IdcSiat/IdcGeneraConstancia.jsf': SimpleNamespace(
            status_code=200, content=pdf
        ),
    }

    with mock.patch.object(SATPortalConstancia, 'login'), \
            mock.patch.object(SATPortalConstancia, 'get', side_effect=lambda url, **kw: get_responses[url.split('?')[0]]), \
            mock.patch.object(SATPortalConstancia, 'form') as form:
        assert portal.generar_constancia() == pdf

    form.assert_called_once()
    action, referer, data = form.call_args.args
    assert action == CONSULTA_TRAMITE_URL
    assert data['formReimpAcuse:tipoTramite_filter'] == ''
    assert data['formReimpAcuse:fechaInicio_input'] == ''
    assert 'formReimpAcuse:fechaInicio_input:' not in data
    assert data['formReimpAcuse:tipoTramite_input'] == '0'
    assert data['javax.faces.source'] == 'formReimpAcuse:j_idt50'
    assert data['formReimpAcuse:j_idt50'] == 'formReimpAcuse:j_idt50'
    assert data['javax.faces.ViewState'] == '-123:456'
    assert 'formReimpAcuse:j_idt47' not in data
    assert 'formReimpAcuse:unchecked' not in data
