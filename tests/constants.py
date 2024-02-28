import os
from os import walk

current_dir = os.path.dirname(__file__)

CFDI_FILES = []

walk_path = os.path.join(current_dir, 'cfdi_ejemplos')
for (dirpath, dirnames, filenames) in walk(walk_path):
    print(dirpath, dirnames)
    rel_path = os.path.relpath(dirpath, walk_path)
    for f in filenames:
        CFDI_FILES.append(os.path.join(rel_path, f))


PERSONAS_FISICAS = [
    'CACX7605101P8',
    'CAÑF770131PA3',
    'FUNK671228PH6',
    'IAÑL750210963',
    'JUFA7608212V6',
    'KAHO641101B39',
    'KICR630120NX3',
    'LIÑI920228KS8',
    'MISC491214B86',
    'RAQÑ7701212M3',
    'WATM640917J45',
    'WERX631016S30',
    'XAMA620210DQ5',
    'XIQB891116QE4',
    'XOJI740919U48',
]

PERSONAS_MORALES = [
    'EKU9003173C9',
    'EWE1709045U0',
    'H&E951128469',
    'HAÑ930228SM9',
    'IIA040805DZ4',
    'IVD920810GU2',
    'IXS7607092R5',
    'JES900109Q90',
    'KIJ0906199R1',
    'L&O950913MSA',
    'OÑO120726RX3',
    'S&S051221SE2',
    'URE180429TM6',
    'XIA190128J61',
    'ZUÑ920208KL4',
]