import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *
from worldmap import WorldMap
from gridpath import get_random_path, num_to_coord


def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # -------------------------------------------------
    # GAME STATE OPTIONS:
    #   "show_path"  -> show path at start
    #   "playing"    -> normal gameplay
    #   "paused"     -> minimap display
    #   "game_over"  -> player dead
    # -------------------------------------------------
    game_state = "show_path"

    # Generate valid path at game start
    path = get_random_path(total_moves=10)

    # Timer for path display
    path_display_time = 3.0  # seconds
    path_timer = 0

    # Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    world = WorldMap()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)
    asteroidfield = AsteroidField()

    # Main loop
    while True:

        # -------------------------
        # EVENT HANDLING
        # -------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:

                # Toggle pause
                if event.key == pygame.K_p:
                    if game_state == "playing":
                        game_state = "paused"
                    elif game_state == "paused":
                        game_state = "playing"

                # Restart
                if event.key == pygame.K_r and game_state == "game_over":
                    return main()

        screen.fill("black")

        # -------------------------------------------------
        # STATE: SHOW PATH AT START
        # -------------------------------------------------
        if game_state == "show_path":

            path_timer += dt

            draw_minimap(screen, world, path, highlight_current=False)

            if path_timer >= path_display_time:
                game_state = "playing"

        # -------------------------------------------------
        # STATE: PLAYING
        # -------------------------------------------------
        elif game_state == "playing":

            updatable.update(dt)

            # -------------------------
            # EDGE TRANSITION LOGIC
            # -------------------------
            moved_sector = False

            if player.position.x < 0:
                world.move_sector(-1, 0)
                player.position.x = SCREEN_WIDTH
                moved_sector = True

            elif player.position.x > SCREEN_WIDTH:
                world.move_sector(1, 0)
                player.position.x = 0
                moved_sector = True

            elif player.position.y < 0:
                world.move_sector(0, -1)
                player.position.y = SCREEN_HEIGHT
                moved_sector = True

            elif player.position.y > SCREEN_HEIGHT:
                world.move_sector(0, 1)
                player.position.y = 0
                moved_sector = True

            if moved_sector:
                print("Entered sector:", world.get_sector())

            # -------------------------
            # COLLISIONS
            # -------------------------
            for a in asteroids:
                if a.collision(player):
                    game_state = "game_over"

            for a in asteroids:
                for s in shots:
                    if s.collision(a):
                        s.kill()
                        a.split()

            # Draw game world
            for obj in drawable:
                obj.draw(screen)

        # -------------------------------------------------
        # STATE: PAUSED (SHOW MINIMAP)
        # -------------------------------------------------
        elif game_state == "paused":

            # Draw frozen world
            for obj in drawable:
                obj.draw(screen)

            # Overlay minimap
            draw_minimap(screen, world, path, highlight_current=True)

        # -------------------------------------------------
        # STATE: GAME OVER
        # -------------------------------------------------
        elif game_state == "game_over":

            for obj in drawable:
                obj.draw(screen)

            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, "white")
            screen.blit(
                text,
                (
                    SCREEN_WIDTH // 2 - text.get_width() // 2,
                    SCREEN_HEIGHT // 2 - text.get_height() // 2
                )
            )

        pygame.display.flip()
        dt = clock.tick(60) / 1000


# -------------------------------------------------
# MINIMAP DRAW FUNCTION
# -------------------------------------------------
def draw_minimap(screen, world, path, highlight_current=True):
    """
    Draws a simple minimap overlay.

    - Shows entire GRID_SIZE x GRID_SIZE grid
    - Highlights path squares
    - Optionally highlights current sector
    """

    map_size = 200
    cell_size = map_size // GRID_SIZE
    offset_x = SCREEN_WIDTH - map_size - 20
    offset_y = 20

    for square in range(1, GRID_SIZE * GRID_SIZE + 1):
        row, col = num_to_coord(square)

        rect = pygame.Rect(
            offset_x + col * cell_size,
            offset_y + row * cell_size,
            cell_size,
            cell_size
        )

        # Highlight path
        if square in path:
            pygame.draw.rect(screen, "blue", rect)
        else:
            pygame.draw.rect(screen, "gray", rect, 1)

    # Highlight current sector
    if highlight_current:
        current_x, current_y = world.get_sector()
        rect = pygame.Rect(
            offset_x + current_x * cell_size,
            offset_y + current_y * cell_size,
            cell_size,
            cell_size
        )
        pygame.draw.rect(screen, "red", rect, 3)

# run main only if file executed directly
if __name__ == "__main__":
    main()