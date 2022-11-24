from importlib.metadata import version, PackageNotFoundError

__title__ = "SAT-CFDI"
__package__ = "satcfdi"

__description__ = "The best open-source python library to generate and process SAT's CFDI"
__git_project__ = "SAT-CFDI/python-satcfdi"
__url__ = f"https://github.com/{__git_project__}"

__docs_url__ = f"https://{__package__}.readthedocs.io"
__docs_badge_url__ = f"https://readthedocs.org/projects/{__package__}/badge"

__author__ = "satcfdi@outlook.com"
__author_email__ = "satcfdi@outlook.com"
__license__ = "MIT License"

try:
    __version__ = version(__package__)
except PackageNotFoundError:
    __version__ = "1.0.0"

__user_agent__ = f"python-{__package__}/{__version__}"
