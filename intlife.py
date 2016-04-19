

DEFAULT_SIZE = 8


class IntLife:
    def __init__(self, seed, *, generations, size):
        self.size = size
        self._cells = None
        self._make_cells()

        if isinstance(seed, int):
            self._board = frozenset(self._cells[i] for i, b in enumerate(reversed(bin(seed)[2:])) if int(b))
        else:
            self._board = frozenset(seed)

        self.generations = generations
        self._neigh = frozenset((i, j) for i in range(-1, 2) for j in range(-1, 2))

        self._neigh_cache = {}
        self._board_cache = {}
        self._int_cache = {}

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
        cache = self._neigh_cache

        if point in cache:
            return cache[point]
        else:
            x, y = point
            size = self.size
            point_neigh = set()

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

                point_neigh.add((xi, yj))

            point_neigh = frozenset(point_neigh)
            cache[point] = point_neigh
            return point_neigh

    def _advance(self):
        board = self._board
        cache = self._board_cache

        if board in cache:
            self._board = cache[board]
        else:
            new_board = set()
            neighbours = self._neighbours

            for point in {n for p in board for n in neighbours(p)}:
                alive_neigh = len(board & neighbours(point))

                if alive_neigh == 3 or (alive_neigh == 4 and point in board):
                    new_board.add(point)

            new_board = frozenset(new_board)
            cache[board] = new_board
            self._board = new_board

    @property
    def int(self):
        cache = self._int_cache
        board = self._board

        if board in cache:
            return cache[board]
        else:
            cells = self._cells
            value = sum(2 ** cells[p] for p in board)
            cache[board] = value
            return value

    @property
    def board(self):
        return self._board


def intlife(seed, generations=None, size=DEFAULT_SIZE):
    yield from IntLife(seed, generations=generations, size=size)


def boardify(number, size=DEFAULT_SIZE):
    return IntLife(number, generations=0, size=size).board


def intify(board, size=DEFAULT_SIZE):
    return IntLife(board, generations=0, size=size).int
