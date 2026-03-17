import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from worldmap import WorldMap
from gridpath import get_random_path, num_to_coord
from planet import *
from wormhole import *
from blackhole import *

def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    font_title = pygame.font.SysFont(None, 96)
    font_prompt = pygame.font.SysFont(None, 36)
    font_status = pygame.font.SysFont(None, 36)

    score = 0
    font_ui = pygame.font.SysFont(None,36)
    score_text = font_ui.render(f"Resources: {score}",True,"white")
    screen.blit(score_text,(20,20))

    # -------------------------------------------------
    # GAME STATE OPTIONS:
    #   "show_title" -> show title 
    #   "show_path"  -> show path at start
    #   "playing"    -> normal gameplay
    #   "paused"     -> minimap display
    #   "game_over"  -> player dead
    # -------------------------------------------------
    game_state = "title"

    # Generate a valid path at game start 
    path = get_random_path()
    print("Generated path:", path)
    path_display_time = 3.0
    path_timer = 0
    path_visible_steps = 0
    path_finished = False

    # Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    planets = pygame.sprite.Group()
    blackholes = pygame.sprite.Group()
    wormholes = pygame.sprite.Group()

    # Containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Planet.containers = (planets,drawable)
    BlackHole.containers = (blackholes,drawable)
    WormHole.containers = (wormholes,drawable)


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

                if game_state == "title":
                    game_state = "show_path"

                elif game_state == "show_path" and path_finished:
                    game_state = "playing"

                # Toggle pause
                elif event.key == pygame.K_p:
                    if game_state == "playing":
                        game_state = "paused"
                    elif game_state == "paused":
                        game_state = "playing"

                # Restart
                if event.key == pygame.K_r and game_state == "game_over":
                    return main()

        screen.fill("black")

        # -------------------------------------------------
        # STATE: TITLE SCREEN
        # -------------------------------------------------
        if game_state == "title":

            title = font_title.render("SPACE MINER", True, "white")
            prompt = font_prompt.render("Press any key to continue", True, "gray")

            screen.blit(
                title,
                (
                    SCREEN_WIDTH // 2 - title.get_width() // 2,
                    SCREEN_HEIGHT // 2 - 100
                )
            )

            screen.blit(
                prompt,
                (
                    SCREEN_WIDTH // 2 - prompt.get_width() // 2,
                    SCREEN_HEIGHT // 2 + 20
                )
            )

        # -------------------------------------------------
        # STATE: SHOW PATH AT START
        # -------------------------------------------------
        elif game_state == "show_path":

            # --------------------------------
            # PATH STILL CALCULATING
            # --------------------------------
            if not path_finished:

                path_timer += dt

                reveal_speed = len(path) / path_display_time
                path_visible_steps = int(path_timer * reveal_speed)

                visible_path = path[:path_visible_steps]

                draw_minimap(screen, world, visible_path, highlight_current=False)

                # animated navicomputer message
                dots = "." * ((pygame.time.get_ticks() // 400) % 4)
                status = f"Navicomputer calculating path{dots}"

                status_text = font_status.render(status, True, "white")

                screen.blit(
                    status_text,
                    (
                        SCREEN_WIDTH // 2 - status_text.get_width() // 2,
                        SCREEN_HEIGHT - 100
                    )
                )

                if path_timer >= path_display_time:
                    path_finished = True

            # --------------------------------
            # PATH FINISHED
            # --------------------------------
            else:

                draw_minimap(screen, world, path, highlight_current=False)

                prompt = font_status.render(
                    "Press any key to continue",
                    True,
                    "white"
                )

                screen.blit(
                    prompt,
                    (
                        SCREEN_WIDTH // 2 - prompt.get_width() // 2,
                        SCREEN_HEIGHT - 100
                    )
                )
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

            # Draw game world
            for obj in drawable:
                obj.draw(screen)

            # Resource collection
            for planet in planets:

                for r in planet.resources:

                    if not r[2]:

                        dot = pygame.Vector2(
                            planet.position.x + r[0],
                            planet.position.y + r[1]
                        )

                    if player.position.distance_to(dot) < 15:

                        r[2] = True
                        score += 1

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

        # highlight path
        if square in path:
            pygame.draw.rect(screen, "blue", rect)

        # draw grid
        pygame.draw.rect(screen, "gray", rect, 1)

    # highlight player sector
    if highlight_current:

        row, col = world.get_sector()   # row first, col second

        rect = pygame.Rect(
            offset_x + col * cell_size,
            offset_y + row * cell_size,
            cell_size,
            cell_size
        )

        pygame.draw.rect(screen, "red", rect, 3)

# run main only if file executed directly
if __name__ == "__main__":
    main()