import logging
import os
from decimal import Decimal
from itertools import repeat, chain
from satcfdi.create.compute import aggregate

module = 'satcfdi'
current_dir = os.path.dirname(__file__)

logging.basicConfig(level=logging.INFO)


def test_aggregate():
    vals = repeat({
        "k1": "A",
        "k2": "B",
        "v1": 10,
        "v2": 20
    }, 3)
    res = aggregate(
        vals,
        keys=("k1", 'k2'),
        values=("v1", "v2"),
    )
    assert res == [{'k1': 'A', 'k2': 'B', 'v1': 30, 'v2': 60}]

    vals = repeat({
        "k1": "A",
        "k2": "B",
        "v1": Decimal(10),
        "v2": Decimal(20)
    }, 3)
    res = aggregate(
        vals,
        keys=("k1", 'k2'),
        values=("v1", "v2"),
        project=("p1", "p2", "p3", "p4")
    )
    assert res == [{'p1': 'A', 'p2': 'B', 'p3': Decimal('30'), 'p4': Decimal('60')}]

    vals = repeat({
        "k1": "A",
        "k2": "B",
        "v1": Decimal(10),
        "v2": Decimal(20)
    }, 3)
    vals2 = repeat({
        "k1": "C",
        "k2": "B",
        "v1": Decimal(10),
        "v2": Decimal(20)
    }, 3)
    res = aggregate(
        chain(vals, vals2),
        keys=("k1", 'k2'),
        values=("v1", "v2"),
        project=("p1", "p2", "p3", "p4")
    )
    assert res == [{'p1': 'A', 'p2': 'B', 'p3': Decimal('30'), 'p4': Decimal('60')},
                   {'p1': 'C', 'p2': 'B', 'p3': Decimal('30'), 'p4': Decimal('60')}] != [{'p1': 'A', 'p2': 'B', 'p3': Decimal('30'), 'p4': Decimal('60')}]
