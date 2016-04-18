
import pytest

import intlife


@pytest.mark.parametrize("board,number", [
    ({(0, 0), (0, 1), (0, 3), (1, 1), (2, 0), (2, 1), (2, 2), (3, 1)}, 3421),
    ({(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)}, 223),
])
def test_intify(board, number):
    assert intlife.intify(board) == number
