
from itertools import chain, product


DEFAULT_SIZE = 8


class IntLife:
    def __init__(self, seed, *, generations, size):
        self.seed = seed
        self.generations = generations
        self.size = size

        self._neigh = {(i, j) for i, j in product(range(-1, 2), repeat=2)}
        self._cells = None
        self.cells()
        self._board = {self._cells[i] for i, b in enumerate(reversed(bin(self.seed)[2:])) if int(b)}

    def __iter__(self):
        if self.generations is None:
            while True:
                self.advance()
                yield self.int
        else:
            count = 0
            while count < self.generations:
                self.advance()
                yield self.int
                count += 1

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = set(value)

    def cells(self):
        cells = {}
        index = 0

        for i in range(self.size):
            for j in range(i):
                tup = (i, j)
                cells[index] = tup
                cells[tup] = index
                index += 1

                tup = (j, i)
                cells[index] = tup
                cells[tup] = index
                index += 1

            tup = (i, i)
            cells[index] = tup
            cells[tup] = index
            index += 1

        self._cells = cells

    def neighbours(self, point):
        x, y = point
        size = self.size

        for i, j in self._neigh:
            xi = x + i
            yj = y + j

            if xi < 0:
                xi += size
            elif xi >= size:
                xi -= size

            if yj < 0:
                yj += size
            elif yj >= size:
                yj -= size

            yield xi, yj

    @property
    def int(self):
        return sum(2**self._cells[p] for p in self._board)

    def advance(self):
        board = self._board
        new_board = set()

        for point in chain.from_iterable(map(self.neighbours, board)):
            alive_neigh = sum(1 for neigh in self.neighbours(point) if neigh in board)

            if alive_neigh == 3 or (alive_neigh == 4 and point in board):
                new_board.add(point)

        self._board = new_board


def intlife(seed, generations=None, size=DEFAULT_SIZE):
    yield from IntLife(seed, generations=generations, size=size)


def boardify(number, size=DEFAULT_SIZE):
    return IntLife(number, generations=0, size=size).board


def intify(board, size=DEFAULT_SIZE):
    il = IntLife(0, generations=0, size=size)
    il.board = board
    return il.int
