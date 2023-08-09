import glob
import logging
import sys
from typing import List, Optional

from .. import render
from ..cfdi import CFDI, CFDIError

logging.basicConfig(level=logging.INFO)
logging.getLogger("weasyprint").setLevel(logging.ERROR)
logging.getLogger("fontTools").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)


def main(args: Optional[List[str]] = None) -> int:
    if args is None:
        args = sys.argv[1:]

    try:
        cmd_name = args[0]
    except IndexError:
        cmd_name = "help"

    match cmd_name:
        case "pdf":
            try:
                file = args[1]
            except IndexError:
                sys.stderr.write("File argument is missing, example: cfdi pdf myfile.xml")
                sys.exit(1)

            for file in glob.iglob(file):
                cfdi = CFDI.from_file(filename=file)
                target = (file[:-4] if file.endswith(".xml") else file) + ".pdf"
                render.pdf_write(cfdi, target=target)
                logger.info(f"PDF created: '{file}'")

        case "html":
            try:
                file = args[1]
            except IndexError:
                sys.stderr.write("File argument is missing, example: cfdi pdf myfile.xml")
                sys.exit(1)

            for file in glob.iglob(file):
                cfdi = CFDI.from_file(filename=file)
                target = (file[:-4] if file.endswith(".xml") else file) + ".html"
                render.html_write(cfdi, target=target)
                logger.info(f"HTML created: '{file}'")

        case "json":
            try:
                file = args[1]
            except IndexError:
                sys.stderr.write("File argument is missing, example: cfdi pdf myfile.xml")
                sys.exit(1)

            for file in glob.iglob(file):
                cfdi = CFDI.from_file(filename=file)
                target = (file[:-4] if file.endswith(".xml") else file) + ".json"
                render.json_write(cfdi, target=target, pretty_print=True)
                logger.info(f"JSON created: '{file}'")

        case "help":
            sys.stdout.write("Looks like you need some help\n")
            sys.stdout.write("Commands:\n")
            sys.stdout.write(" pdf       creates a pdf file\n")
            sys.stdout.write(" html      creates a html file\n")
            sys.stdout.write(" json      creates a json file\n")

        case _:
            raise CFDIError("Invalid Command")

    return 0
