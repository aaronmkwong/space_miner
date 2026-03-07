import random
from constants import GRID_SIZE, START_ROW, START_COL


def num_to_coord(n):
    """
    Convert a grid square number (1 to GRID_SIZE^2)
    into (row, col) coordinates.
    """
    return ((n - 1) // GRID_SIZE, (n - 1) % GRID_SIZE)


def coord_to_num(r, c):
    """
    Convert (row, col) coordinates back into a grid number.
    """
    return r * GRID_SIZE + c + 1


def neighbors(n):
    """
    Return all valid adjacent squares (up/down/left/right).

    Movement is restricted to stay inside the grid bounds.
    No diagonal movement allowed.
    """
    r, c = num_to_coord(n)

    possible_moves = [
        (r - 1, c),  # up
        (r + 1, c),  # down
        (r, c - 1),  # left
        (r, c + 1)   # right
    ]

    valid = []

    for nr, nc in possible_moves:
        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
            valid.append(coord_to_num(nr, nc))

    return valid


def generate_paths(total_moves=10):
    """
    Generate all valid path sequences that:

    - Start at (START_ROW, START_COL)
    - Move only to adjacent squares
    - Do NOT revisit squares
    - First 3 moves are forced to the right
    - Return to the start square in exactly total_moves moves

    Returns:
        A list of valid path sequences.
    """

    # Ensure grid is large enough for 3-right movement
    if START_COL + 3 >= GRID_SIZE:
        raise ValueError("Grid too small to force 3 moves to the right.")

    start_square = coord_to_num(START_ROW, START_COL)

    # Build forced prefix dynamically
    forced_prefix = [start_square]
    current = start_square

    for _ in range(3):
        r, c = num_to_coord(current)
        c += 1  # move right
        current = coord_to_num(r, c)
        forced_prefix.append(current)

    results = []

    def dfs(path, visited):
        """
        Recursive Depth-First Search to explore all valid simple paths.

        path    = current path list
        visited = set of visited squares (prevents revisits)
        """

        current_square = path[-1]

        # If required move count reached
        if len(path) - 1 == total_moves:
            # Check if we can legally return to start
            if start_square in neighbors(current_square):
                results.append(path + [start_square])
            return

        # Explore all adjacent squares
        for nxt in neighbors(current_square):
            if nxt not in visited:
                visited.add(nxt)
                dfs(path + [nxt], visited)
                visited.remove(nxt)  # backtrack

    dfs(forced_prefix, set(forced_prefix))

    return results


def get_random_path(total_moves=10):
    """
    Convenience function for game startup.

    Generates all valid paths and returns one random path.
    """
    paths = generate_paths(total_moves)
    return random.choice(paths) if paths else []