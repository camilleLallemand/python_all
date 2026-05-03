from maze_generator import Maze, MazeGenerator, CellStatus
from display import run, place_42, show_path
from exporter import export

# entry (x.y) mais maze.matrix[y][x]


def build_maze() -> tuple[Maze, MazeGenerator]:
    x_start = 1
    y_start = 0
    x_end = 0
    y_end = 5
    maze = Maze(
        width=10, height=6, seed=110, perfect=True,
        entry=(x_start, y_start), end=(x_end, y_end), out_file="maze.txt",
    )
    if ((x_end == x_start and y_end == y_start)
        or x_end >= maze.width or y_end >= maze.height
            or x_start > maze.width or y_start >= maze.height):
        print("invalid start/end coord")
        return (None, None)
    maze.matrix[y_start][x_start].status = CellStatus.START
    maze.matrix[y_end][x_end].status = CellStatus.EXIT
    place_42(maze)
    if (maze.matrix[y_start][x_start].status == CellStatus.FORTY or maze.matrix[y_end]
            [x_end].status == CellStatus.FORTY):
        print("invalid start/end placed on forty")
        return (None, None)

    gen = MazeGenerator(maze)
    gen.generate()
    gen.solve()
    show_path(maze, visible=True)
    return maze, gen


if __name__ == "__main__":
    maze, gen = build_maze()
    if maze and gen:

        export(maze, maze.out_file)
        run(maze, gen)
