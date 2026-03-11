"""Shared pytest configuration and fixtures for satcfdi tests."""

import os
import logging

import pytest

from satcfdi.cfdi import CFDI
from satcfdi.models import Signer


TESTS_DIR = os.path.dirname(__file__)


@pytest.fixture(scope="session")
def test_data_dir():
    """Return the path to the tests directory containing test data."""
    return TESTS_DIR


@pytest.fixture(scope="session")
def cfdi_ejemplos_dir():
    """Return the path to the CFDI examples directory."""
    return os.path.join(TESTS_DIR, "cfdi_ejemplos")


@pytest.fixture(scope="session")
def csd_dir():
    """Return the path to the CSD certificates directory."""
    return os.path.join(TESTS_DIR, "csd")


@pytest.fixture
def sample_cfdi_v40(cfdi_ejemplos_dir):
    """Load a sample CFDI v4.0 for testing."""
    return CFDI.from_file(
        os.path.join(cfdi_ejemplos_dir, "comprobante40", "cfdv40-ejemplo.xml")
    )


@pytest.fixture
def sample_cfdi_v33(cfdi_ejemplos_dir):
    """Load a sample CFDI v3.3 for testing."""
    return CFDI.from_file(
        os.path.join(cfdi_ejemplos_dir, "comprobante33", "cfdv33-ejemplo.xml")
    )


@pytest.fixture
def tmp_output_dir(tmp_path):
    """Provide a temporary directory for test output files."""
    output = tmp_path / "output"
    output.mkdir()
    return output


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "network: marks tests that require network access")
    config.addinivalue_line("markers", "pac: marks tests that interact with PAC providers")
    config.addinivalue_line("markers", "render: marks tests for PDF/HTML rendering")
    config.addinivalue_line("markers", "create: marks tests for CFDI creation")
