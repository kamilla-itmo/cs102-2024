from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """
    Удаляет стену в лабиринте в заданной клетке.

    :param grid: текущий лабиринт
    :param coord: координаты текущей клетки
    :return: обновленный лабиринт
    """
    y, x = coord

    directions = []

    y, x = coord
    height = len(grid) - 1
    width = len(grid[0]) - 1

    directions = [(-1, 0), (0, 1)]
    rand_index = randint(0, len(directions) - 1)
    dy, dx = directions[rand_index]

    if y + 2 * dy < 0 or x + 2 * dx >= len(grid[0]):
        rand_index = abs(1 - rand_index)
        dy, dx = directions[rand_index]
        if y + 2 * dy < 0 or x + 2 * dx >= len(grid[0]):
            return grid

    wall_y, wall_x = y + dy, x + dx
    next_y, next_x = y + 2 * dy, x + 2 * dx
    grid[wall_y][wall_x] = " "
    grid[next_y][next_x] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """
    result = create_grid(rows, cols)
    empty_cells = []
    for y in range(len(result)):
        for x in range(len(result[y])):
            if y % 2 == 1 and x % 2 == 1:
                result[y][x] = " "
                empty_cells.append((y, x))

    for coord in empty_cells:
        result = remove_wall(result, coord)

    if random_exit:
        y_enter = randint(0, rows - 1)
        y_exit = randint(0, rows - 1)

        if y_enter in (0, rows - 1):
            x_enter = randint(0, cols - 1)
        else:
            x_enter = choice((0, cols - 1))

        if y_exit in (0, rows - 1):
            x_exit = randint(0, cols - 1)
        else:
            x_exit = choice((0, cols - 1))

    else:
        y_enter, x_enter = 0, cols - 2
        y_exit, x_exit = rows - 1, 1

    result[y_enter][x_enter] = "X"
    result[y_exit][x_exit] = "X"

    return result


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = set()
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for y in range(cols):
        if grid[0][y] == "X":
            exits.add((0, y))
        if grid[rows - 1][y] == "X":
            exits.add((rows - 1, y))

    for x in range(rows):
        if grid[x][0] == "X":
            exits.add((x, 0))
        if grid[x][cols - 1] == "X":
            exits.add((x, cols - 1))

    return sorted(exits)


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    rows = len(grid)
    cols = len(grid[0])

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == k:
                for dy, dx in directions:
                    y_diff = y + dy
                    x_diff = x + dx

                    if 0 <= y_diff < rows and 0 <= x_diff < cols and grid[y_diff][x_diff] == 0:
                        grid[y_diff][x_diff] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """

    y_exit, x_exit = exit_coord
    steps = 0

    while grid[y_exit][x_exit] == 0:
        steps += 1
        grid = make_step(grid, steps)

    route = [(y_exit, x_exit)]
    k = int(grid[y_exit][x_exit])
    y_current, x_current = y_exit, x_exit

    while grid[y_current][x_current] != 1 and k > 0:
        if (y_current + 1 < len(grid)) and (grid[y_current + 1][x_current] == k - 1):
            y_current += 1
        elif (y_current - 1 >= 0) and (grid[y_current - 1][x_current] == k - 1):
            y_current -= 1
        elif (x_current + 1 < len(grid[0])) and (grid[y_current][x_current + 1] == k - 1):
            x_current += 1
        elif (x_current - 1 >= 0) and (grid[y_current][x_current - 1] == k - 1):
            x_current -= 1
        else:
            break
        route.append((y_current, x_current))
        k -= 1

    if len(route) != grid[y_exit][x_exit]:
        grid[route[-1][0]][route[-1][1]] = " "
        route.pop()
        if route:
            y_next, x_next = route[-1]
            shortest_path(grid, (y_next, x_next))

    return route


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    if (
        (x == 0 and y == 0)
        or (x == 0 and y == cols - 1)
        or (x == rows - 1 and y == 0)
        or (x == rows - 1 and y == cols - 1)
    ):
        if grid[x + (1 if x == 0 else -1)][y] == "■" and grid[x][y + (1 if y == 0 else -1)] == "■":
            return True
    if x == 0 or x == rows - 1 or y == 0 or y == cols - 1:
        wall_count = 0
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for nx, ny in neighbors:
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "■":
                wall_count += 1
        if wall_count >= 3:
            return True
        if wall_count == 2:
            for nx, ny in neighbors:
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == " ":
                    return False

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)
    if len(exits) > 1:
        if encircled_exit(grid, exits[0]) or encircled_exit(grid, exits[1]):
            return grid, None

        grid_copy = deepcopy(grid)
        y_exit, x_exit = exits[0]
        grid[y_exit][x_exit] = 1

        for y in range(len(grid_copy)):
            for x in range(len(grid_copy[0])):
                if grid[y][x] in (" ", "X"):
                    grid[y][x] = 0

        path = shortest_path(grid, exits[1])
        return grid_copy, path
    else:
        return grid, exits


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid
