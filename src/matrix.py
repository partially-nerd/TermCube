from typing import override


class Matrix:
    face: list[list[int]]
    m: int
    n: int

    def __init__(self, face: list[list[int]]) -> None:
        self.face = face
        self.m = self.face.__len__()
        self.n = self.face[0].__len__()

    def ROW(self, y: int, set: list[int] | None = None) -> list[int]:
        if y >= self.m: return []
        if set is not None:
            if set.__len__() != self.n: return []
            self.face[y] = set
        return self.face[y]

    def COL(self, x: int, set: list[int] | None = None) -> list[int]:
        if x >= self.n: return []
        if set is not None:
            if set.__len__() != self.m: return []
            for y in range(self.m):
                self.face[y][x] = set[y]
        return [self.face[y][x] for y in range(self.m)]

    def VERT_FLIP(self) -> Matrix:
        return Matrix([self.ROW(self.m - 1 - y) for y in range(self.m)])

    def HORI_FLIP(self) -> Matrix:
        ret_val: Matrix = Matrix([[0 for _ in range(self.n)] for _ in range(self.m)])
        for y in range(self.n):
            _=ret_val.COL(self.n - 1 - y, self.COL(y))
        return ret_val

    def CWR(self) -> Matrix:
        ret_val: Matrix = Matrix([[0 for _ in range(self.n)] for _ in range(self.m)])
        for y in range(self.m):
            _=ret_val.COL(self.m - 1 - y, self.ROW(y))
        return ret_val

    def CCWR(self) -> Matrix:
        ret_val: Matrix = Matrix([[0 for _ in range(self.n)] for _ in range(self.m)])
        for y in range(self.m):
            _=ret_val.ROW(y, self.COL(self.n - 1 - y))
        return ret_val

    @override
    def __repr__(self) -> str:
        out: str = ""
        for row in self.face:
            out += ' '.join([str(i) for i in row]) + "\n"
        return out

    @override
    def __str__(self) -> str:
        out: str = ""
        for row in self.face:
            out += ' '.join([str(i) for i in row]) + "\n"
        return out
