from __future__ import annotations
import os
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maze_generator import Maze, MazeGenerator

from maze_generator import CellStatus, NORTH, EAST, SOUTH, WEST

RESET = "\033[0m"


def ansi(code: str) -> str:
    return f"\033[{code}m"


@dataclass
class ColorScheme:
    name: str
    wall: str
    empty: str
    start: str
    exit: str
    path: str
    forty: str


SCHEMES: list[ColorScheme] = [
    ColorScheme("Classic", ansi("37"), ansi("90"), ansi("92"),
                ansi("91"), ansi("93"), ansi("94")),
    ColorScheme("Neon", ansi("95"), ansi("90"), ansi("96"),
                ansi("91"), ansi("92"), ansi("93")),
    ColorScheme("Ice", ansi("94"), ansi("37"), ansi("96"),
                ansi("97"), ansi("91"), ansi("36")),
    ColorScheme("Lava", ansi("31"), ansi("90"), ansi("93"),
                ansi("97"), ansi("34"), ansi("33")),
    ColorScheme("Forest", ansi("32"), ansi("90"), ansi("93"),
                ansi("91"), ansi("97"), ansi("33")),
]

FORTY_PATTERN: list[list[int]] = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]
PAT_H, PAT_W = 5, 7

CELL_CHAR: dict[CellStatus, str] = {
    CellStatus.EMPTY: "·",
    CellStatus.START: "S",
    CellStatus.EXIT: "E",
    CellStatus.PATH: "*",
    CellStatus.FORTY: "█",
}


def place_42(maze: Maze) -> None:
    if maze.width < PAT_W or maze.height < PAT_H + 1:
        print(f"[42] Maze too small — pattern skipped (min {PAT_W}x{PAT_H}).")
        maze.forty = False
        return
    or_ = (maze.height - PAT_H) // 2
    oc = (maze.width - PAT_W) // 2
    for pr, row in enumerate(FORTY_PATTERN):
        for pc, val in enumerate(row):
            if val:
                c = maze.matrix[or_ + pr][oc + pc]
                c.walls, c.locked, c.status = 0xF, True, CellStatus.FORTY
    maze.forty = True


def _color(status: CellStatus, scheme: ColorScheme) -> str:
    return {
        CellStatus.EMPTY: scheme.empty,
        CellStatus.START: scheme.start,
        CellStatus.EXIT: scheme.exit,
        CellStatus.PATH: scheme.path,
        CellStatus.FORTY: scheme.forty,
    }.get(status, scheme.empty)


def render(maze: Maze, scheme: ColorScheme) -> str:
    lines: list[str] = []
    w = scheme.wall
    for row in range(maze.height):
        top = ""
        bot = ""
        for col in range(maze.width):
            c = maze.matrix[row][col]
            top += w + "+" + (w + "-" if c.has_wall(NORTH) else " ")
            bot += (w + "|" if c.has_wall(WEST) else " ")
            bot += _color(c.status, scheme) + CELL_CHAR[c.status]
        last = maze.matrix[row][maze.width - 1]
        top += w + "+"
        bot += w + "|" if last.has_wall(EAST) else " "
        lines += [top + RESET, bot + RESET]
    bot = ""
    for col in range(maze.width):
        c = maze.matrix[maze.height - 1][col]
        bot += w + "+" + (w + "-" if c.has_wall(SOUTH) else " ")
    lines.append(bot + w + "+" + RESET)
    return "\n".join(lines)


def display(maze: Maze, scheme: ColorScheme) -> None:
    os.system("clear")
    print("  [D] Theme  [R] Regenerate  [P] Path  [Q] Quit\n")
    if (maze.forty):
        print("Forty is real, rush b")
    else:
        print("      Forty statut: Cykq BLYAT no forty here\n")
    print(render(maze, scheme))


def show_path(maze: Maze, visible: bool) -> None:
    skip = {CellStatus.START, CellStatus.EXIT, CellStatus.FORTY}
    for col, row in maze.solution:
        c = maze.matrix[row][col]
        if c.status not in skip:
            c.status = CellStatus.PATH if visible else CellStatus.EMPTY


def run(maze: Maze, gen: MazeGenerator) -> None:
    import tty
    import termios

    idx = 0
    path_on = False

    def read_key() -> str:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    while True:
        display(maze, SCHEMES[idx])
        key = read_key()
        if key == "q":
            print(RESET + "\nGoodbye!")
            break
        elif key == "d":
            idx = (idx + 1) % len(SCHEMES)
        elif key == "p":
            path_on = not path_on
            show_path(maze, path_on)
        elif key == "r":
            path_on = False
            gen.regenerate()
