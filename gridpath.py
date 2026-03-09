import random
from constants import GRID_SIZE, START_ROW, START_COL


def num_to_coord(n):
    return ((n - 1) // GRID_SIZE, (n - 1) % GRID_SIZE)


def coord_to_num(r, c):
    return r * GRID_SIZE + c + 1


def get_random_path():
    """
    Generates a guaranteed valid loop path.

    Rules:
    - Start at START_ROW, START_COL
    - First 3 moves go right
    - Then create a rectangular loop with random size
    - Return to start
    """

    r = START_ROW
    c = START_COL

    path = [coord_to_num(r, c)]

    # ---- forced 3 moves right ----
    for _ in range(3):
        c += 1
        path.append(coord_to_num(r, c))

    start_loop_col = c

    # ---- choose random loop size ----
    max_height = GRID_SIZE - r - 1
    max_width = start_loop_col

    height = random.randint(1, max(1, max_height))
    width = random.randint(1, max(1, max_width))

    # ---- move down ----
    for _ in range(height):
        r += 1
        path.append(coord_to_num(r, c))

    # ---- move left ----
    for _ in range(width):
        c -= 1
        path.append(coord_to_num(r, c))

    # ---- move up ----
    for _ in range(height):
        r -= 1
        path.append(coord_to_num(r, c))

    # ---- move right back to start column ----
    while c < START_COL:
        c += 1
        path.append(coord_to_num(r, c))

    return path