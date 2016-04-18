

DEFAULT_SIZE = 8


class IntLife:
    def __init__(self, seed, *, generations, size):
        self.size = size
        self._cells = None
        self._make_cells()

        try:
            self._board = set(seed)
        except TypeError:
            self._board = {self._cells[i] for i, b in enumerate(reversed(bin(seed)[2:])) if int(b)}

        self.generations = generations
        self._neigh = {(i, j) for i in range(-1, 2) for j in range(-1, 2)}

    def __iter__(self):
        if self.generations is None:
            while True:
                self._advance()
                yield self.int
        else:
            count = 0
            while count < self.generations:
                self._advance()
                yield self.int
                count += 1

    def _make_cells(self):
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

    def _neighbours(self, point):
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

    def _advance(self):
        board = self._board
        new_board = set()
        neighbours = self._neighbours

        for point in (n for p in board for n in neighbours(p)):
            alive_neigh = sum(1 for neigh in neighbours(point) if neigh in board)

            if alive_neigh == 3 or (alive_neigh == 4 and point in board):
                new_board.add(point)

        self._board = new_board

    @property
    def int(self):
        return sum(2 ** self._cells[p] for p in self._board)

    @property
    def board(self):
        return self._board


def intlife(seed, generations=None, size=DEFAULT_SIZE):
    yield from IntLife(seed, generations=generations, size=size)


def boardify(number, size=DEFAULT_SIZE):
    return IntLife(number, generations=0, size=size).board


def intify(board, size=DEFAULT_SIZE):
    return IntLife(board, generations=0, size=size).int

