from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maze_generator import Maze

from maze_generator import DELTA, DIRS
from maze_generator import NORTH, EAST, SOUTH, WEST

DIR_LETTER: dict[int, str] = {NORTH: "N", EAST: "E", SOUTH: "S", WEST: "W"}


def _path_str(maze: Maze) -> str:
    if not maze.solution:
        return ""
    full = [maze.entry] + maze.solution + [maze.end]
    out = ""
    for i in range(len(full) - 1):
        col, row = full[i]
        nc, nr = full[i + 1]
        dc, dr = nc - col, nr - row
        for d, (ddc, ddr) in DELTA.items():
            if ddc == dc and ddr == dr:
                out += DIR_LETTER[d]
                break
    return out


def export(maze: Maze, path: str) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            for row in range(maze.height):
                f.write("".join(
                    maze.matrix[row][col].hex_value()
                    for col in range(maze.width)
                ) + "\n")
            f.write("\n")
            ec, er = maze.entry
            xc, xr = maze.end
            f.write(f"{ec},{er}\n{xc},{xr}\n{_path_str(maze)}\n")
    except OSError as e:
        print(f"[Export] Error: {e}")
