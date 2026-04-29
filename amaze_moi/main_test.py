from maze_generator import Maze, MazeGenerator, CellStatus
from display import run, place_42, show_path
from exporter import export


def build_maze() -> tuple[Maze, MazeGenerator]:
    maze = Maze(
        width=50, height=20, seed=110, perfect=False,
        entry=(0, 0), end=(49, 19), out_file="maze.txt",
    )
    maze.matrix[0][0].status = CellStatus.START
    maze.matrix[19][49].status = CellStatus.EXIT
    place_42(maze)
    gen = MazeGenerator(maze)
    gen.generate()
    gen.solve()
    show_path(maze, visible=True)
    return maze, gen


if __name__ == "__main__":
    maze, gen = build_maze()
    export(maze, maze.out_file)
    run(maze, gen)
