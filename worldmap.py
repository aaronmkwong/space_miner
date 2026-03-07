from constants import GRID_SIZE, START_COL, START_ROW


class WorldMap:
    """
    Manages the player's position within the 2D world grid.

    Each grid cell corresponds to one sector (one screen of gameplay).
    The world size is GRID_SIZE x GRID_SIZE.
    """

    def __init__(self):
        """
        Initialize world position at the configured start location.
        """
        self.world_x = START_COL
        self.world_y = START_ROW

    def move_sector(self, dx, dy):
        """
        Move to a new sector.

        dx = horizontal movement (-1 left, +1 right)
        dy = vertical movement (-1 up, +1 down)

        Movement is clamped to remain within grid bounds.
        """

        self.world_x = max(0, min(GRID_SIZE - 1, self.world_x + dx))
        self.world_y = max(0, min(GRID_SIZE - 1, self.world_y + dy))

    def get_sector(self):
        """
        Return current sector coordinates as (x, y).
        Useful for:
            - debugging
            - minimap rendering
            - path validation
        """
        return self.world_x, self.world_y

    def seed_sector(self):
        """
        Generate a deterministic random seed based on sector location.

        This allows procedural generation where:
            The same sector always produces the same asteroid layout.
        """
        return self.world_x * 100 + self.world_y

    def is_within_bounds(self, x, y):
        """
        Check whether a sector coordinate is inside the world grid.
        """
        return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE