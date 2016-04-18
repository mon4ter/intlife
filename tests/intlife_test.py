
from itertools import repeat, count
from random import randrange

import pytest

import intlife


@pytest.mark.parametrize("number", map(randrange, repeat(2**64, times=10)))
def test_conversion(number):
    assert intlife.intify(intlife.boardify(number)) == number


GLIDER = [
    4548,
    20832,
    28936,
    61504,
    2154624,
    10530816,
    14713088,
    31465472,
    4324343808,
    21497905152,
    30081581056,
    64428703744,
    35244510019584,
    175969105084416,
    246324981137408,
    527774171267072,
    1153414102995959808,
    5764994551127212032,
    8070732041584377856,
    17293892937846882304,
    16141041870703689728,
    12682699569348214784,
    9225342430411227136,
    2307531927793434625,
    4615626668101337089,
    3377768440004613,
    9225623836668461063,
    3377699720527886,
    562949953421358,
    2251799813685418,
    233,
    482
]


@pytest.mark.parametrize("seed,number,generations", zip(repeat(GLIDER[-1]), GLIDER, count(1)))
def test_glider(seed, number, generations):
    result = None

    for result in intlife.intlife(seed, generations=generations):
        pass

    assert result == number


def test_iterator():
    iterator = intlife.intlife(15)

    for index in range(100):
        assert next(iterator) == 15
