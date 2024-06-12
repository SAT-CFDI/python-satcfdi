import os
import setuptools

about = {}
current_dir = os.path.abspath(os.path.dirname(__file__))
package_dir = 'satcfdi'

with open(os.path.join(current_dir, package_dir, "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)

package = about["__package__"]

packages = setuptools.find_packages(
    exclude=["contrib", "docs", "tests"],
)

version = os.environ.get('RELEASE_VERSION', about["__version__"])

setuptools.setup(
    name=package,  # installation
    version=version,
    author=about["__author__"],
    author_email=about["__author__"],
    description=about["__description__"],
    long_description=open('readme.rst', 'r', encoding='utf-8').read(),
    long_description_content_type="text/x-rst",
    url=about["__url__"],
    project_urls={
        "Documentation": about["__docs_url__"],
        "Source": about["__url__"],
        # "Changelog": about["__change_log_url__"],
    },
    license=about["__license__"],
    keywords=[
        'cfdi',
        'sat',
        'facturación',
        'comprobante',
        'retenciones',
        'nómina',
        'pagos',
        'carta porte',
        'contabilidad',
        'e-invoicing',
        'DIOT'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Spanish",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ],
    python_requires='>=3.11',
    package_dir={package: package_dir},
    packages=packages,
    package_data={
        package: [
            "diot/*",
            "render/templates/*",
            "transform/schemas/*",
            "transform/schemas/*/*",
            "transform/schemas/*/*/*",
            "transform/schemas/*/*/*/*",
            "transform/schemas/*/*/*/*/*",
            "transform/schemas/*/*/*/*/*/*",
            "transform/schemas/*/*/*/*/*/*/*",
            "transform/CertsProd.zip",
            "catalogs/catalogs.db",
            "pacs/sat_templates/*",
        ],
    },
    install_requires=[
        'jinja2 >= 3.0.0',
        'lxml >= 4.9.0',
        'weasyprint >= 57.0',
        'requests >= 2.0.0',
        'cryptography >= 39.0.0, < 43',
        'pytz >= 2022.5',
        'xlsxwriter >= 3.0.0',
        'pyOpenSSL >= 22.0.0',
        'qrcode >= 7.3.0',
        'tabulate >= 0.9.0',
        'packaging >= 21.0',
        'beautifulsoup4 > 4.11.0'
    ],
    # tests_require=test_deps,
    entry_points={
        "console_scripts": [
            f"{package}={package}.cli.main:main"
        ],
    },
    # extras={
    #     'test': test_deps,
    # },
    extras_require={
        'test': [
            'coverage',
            'pytest',
            'PyYAML'
        ],
        'docs': [
            'Sphinx >= 5.3.0',
            'sphinx-rtd-theme >= 1.1.1'
        ]
    }
)
