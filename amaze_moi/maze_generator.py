from __future__ import annotations
import random
import sys
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

sys.setrecursionlimit(10000)

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

OPPOSITE: dict[int, int] = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
DELTA: dict[int, tuple[int, int]] = {
    NORTH: (0, -1), EAST: (1, 0), SOUTH: (0, 1), WEST: (-1, 0)
}
DIRS: list[int] = [NORTH, EAST, SOUTH, WEST]


def move(col: int, row: int, d: int) -> tuple[int, int]:
    dc, dr = DELTA[d]
    return col + dc, row + dr


class CellStatus(str, Enum):
    EMPTY = "empty"
    START = "start"
    EXIT = "exit"
    PATH = "path"
    FORTY = "forty"


@dataclass
class Cell:
    walls: int = 0b1111
    status: CellStatus = CellStatus.EMPTY
    locked: bool = False

    def has_wall(self, d: int) -> bool:
        return bool(self.walls & d)

    def open_wall(self, d: int) -> None:
        if not self.locked:
            self.walls &= ~d

    def close_wall(self, d: int) -> None:
        if not self.locked:
            self.walls |= d

    def hex_value(self) -> str:
        return format(self.walls, 'X')


@dataclass
class Maze:
    width: int
    height: int
    seed: Optional[int] = None
    perfect: bool = True
    entry: tuple[int, int] = (0, 0)
    end: tuple[int, int] = (0, 0)
    matrix: list[list[Cell]] = field(default_factory=list)
    solution: list[tuple[int, int]] = field(default_factory=list)
    forty: bool = False
    out_file: str = "maze.txt"

    def __post_init__(self) -> None:
        if not self.matrix:
            self.matrix = [
                [Cell() for _ in range(self.width)]
                for _ in range(self.height)
            ]

    def cell(self, col: int, row: int) -> Optional[Cell]:
        if 0 <= col < self.width and 0 <= row < self.height:
            return self.matrix[row][col]
        return None

    def open_passage(self, col: int, row: int, d: int) -> None:
        c = self.cell(col, row)
        if c is None:
            return
        nc, nr = move(col, row, d)
        nb = self.cell(nc, nr)
        if c and not c.locked:
            c.open_wall(d)
        if nb and not nb.locked:
            nb.open_wall(OPPOSITE[d])


class MazeGenerator:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self._seed = random.Random(maze.seed)

    def _rand_dirs(self) -> list[int]:
        dirs = DIRS.copy()
        self._seed.shuffle(dirs)
        return dirs

    def generate(self) -> None:
        visited: set[tuple[int, int]] = set()
        self._reset()
        sc, sr = self.maze.entry
        self._dfs(sc, sr, visited)
        self._connect(visited)
        if not self.maze.perfect:
            self._add_loops()
        self._seal_borders()

    def solve(self) -> None:
        start, end = self.maze.entry, self.maze.end
        queue: deque[tuple[int, int]] = deque([start])
        prev: dict[tuple[int, int], Optional[tuple[int, int]]] = {start: None}
        while queue:
            col, row = queue.popleft()
            if (col, row) == end:
                break
            for d in DIRS:
                if self.maze.matrix[row][col].has_wall(d):
                    continue
                nc, nr = move(col, row, d)
                if (nc, nr) in prev:
                    continue
                nb = self.maze.cell(nc, nr)
                if nb is None:
                    continue
                prev[(nc, nr)] = (col, row)
                queue.append((nc, nr))
        if end not in prev:
            return
        path: list[tuple[int, int]] = []
        cur: Optional[tuple[int, int]] = end
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        self.maze.solution = [p for p in path if p != start and p != end]

    def regenerate(self) -> None:
        from display import place_42
        from exporter import export
        self.maze.seed = self._seed.randint(0, 999999)
        self._seed = random.Random(self.maze.seed)
        self._clear()
        place_42(self.maze)
        self.generate()
        self.solve()
        if self.maze.out_file:
            export(self.maze, self.maze.out_file)

    def _reset(self) -> None:
        for row in range(self.maze.height):
            for col in range(self.maze.width):
                c = self.maze.matrix[row][col]
                if not c.locked:
                    c.walls = 0xF

    def _clear(self) -> None:
        for row in range(self.maze.height):
            for col in range(self.maze.width):
                c = self.maze.matrix[row][col]
                c.locked, c.status, c.walls = False, CellStatus.EMPTY, 0xF
        ec, er = self.maze.entry
        xc, xr = self.maze.end
        self.maze.matrix[er][ec].status = CellStatus.START
        self.maze.matrix[xr][xc].status = CellStatus.EXIT
        self.maze.solution = []

    def _dfs(self, col: int, row: int, visited: set[tuple[int, int]]) -> None:
        visited.add((col, row))
        for d in self._rand_dirs():
            nc, nr = move(col, row, d)
            nb = self.maze.cell(nc, nr)
            if nb is None or (nc, nr) in visited or nb.locked:
                continue
            if self._opens_3x3(col, row, nc, nr):
                continue
            self.maze.open_passage(col, row, d)
            self._dfs(nc, nr, visited)

    def _opens_3x3(self, col: int, row: int, nc: int, nr: int) -> bool:
        mc, mr = min(col, nc), min(row, nr)
        for rs in range(mr - 2, mr + 1):
            for cs in range(mc - 2, mc + 1):
                if self._is_3x3(cs, rs, col, row, nc, nr):
                    return True
        return False

    def _is_3x3(
        self, cs: int, rs: int,
        col: int, row: int, nc: int, nr: int
    ) -> bool:
        for r in range(rs, rs + 3):
            for c in range(cs, cs + 3):
                if self.maze.cell(c, r) is None:
                    return False
                if self.maze.matrix[r][c].locked:
                    return False
        for r in range(rs, rs + 3):
            for c in range(cs, cs + 2):
                sim = (
                    (c == col and r == row and c + 1 == nc and r == nr)
                    or (c == nc and r == nr and c + 1 == col and r == row)
                )
                if not sim and self.maze.matrix[r][c].has_wall(EAST):
                    return False
        for r in range(rs, rs + 2):
            for c in range(cs, cs + 3):
                sim = (
                    (c == col and r == row and c == nc and r + 1 == nr)
                    or (c == nc and r == nr and c == col and r + 1 == row)
                )
                if not sim and self.maze.matrix[r][c].has_wall(SOUTH):
                    return False
        return True

    def _connect(self, visited: set[tuple[int, int]]) -> None:
        changed = True
        while changed:
            changed = False
            for row in range(self.maze.height):
                for col in range(self.maze.width):
                    if (col,
                            row) in visited or self.maze.matrix[row][col].locked:
                        continue
                    for d in self._rand_dirs():
                        nc, nr = move(col, row, d)
                        nb = self.maze.cell(nc, nr)
                        if (nc, nr) not in visited or nb is None or nb.locked:
                            continue
                        self.maze.open_passage(col, row, d)
                        visited.add((col, row))
                        changed = True
                        break

    def _add_loops(self) -> None:
        extra = max(1, (self.maze.width * self.maze.height) // 5)
        candidates: list[tuple[int, int, int]] = []
        for row in range(self.maze.height):
            for col in range(self.maze.width):
                if self.maze.matrix[row][col].locked:
                    continue
                for d in [EAST, SOUTH]:
                    nc, nr = move(col, row, d)
                    nb = self.maze.cell(nc, nr)
                    if nb is None or nb.locked:
                        continue
                    if self.maze.matrix[row][col].has_wall(d):
                        candidates.append((col, row, d))
        self._seed.shuffle(candidates)
        opened = 0
        for col, row, d in candidates:
            if opened >= extra:
                break
            nc, nr = move(col, row, d)
            if not self._opens_3x3(col, row, nc, nr):
                self.maze.open_passage(col, row, d)
                opened += 1

    def _seal_borders(self) -> None:
        for col in range(self.maze.width):
            self.maze.matrix[0][col].close_wall(NORTH)
            self.maze.matrix[self.maze.height - 1][col].close_wall(SOUTH)
        for row in range(self.maze.height):
            self.maze.matrix[row][0].close_wall(WEST)
            self.maze.matrix[row][self.maze.width - 1].close_wall(EAST)
