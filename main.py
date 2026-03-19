import pygame
from constants import *
from player import *
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
    
    # -------------------------------------------------
    # GAME STATE OPTIONS:
    #   "show_title" -> show title 
    #   "show_path"  -> show path at start
    #   "playing"    -> normal gameplay
    #   "paused"     -> minimap display
    #   "game_over"  -> player dead
    # -------------------------------------------------
    game_state = "title"

    # GENERATE VALID PATH AT GAMESTART
    path = get_random_path()
    print("Generated path:", path)
    path_display_time = 3.0
    path_timer = 0
    path_visible_steps = 0
    path_finished = False

    # SPRITE GROUPS
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    planets = pygame.sprite.Group()
    blackholes = pygame.sprite.Group()
    wormholes = pygame.sprite.Group()

    # CONTAINERS
    Player.containers = (updatable, drawable)
    Planet.containers = (planets,drawable)
    BlackHole.containers = (blackholes,drawable)
    WormHole.containers = (wormholes,drawable)

    world = WorldMap()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)

    # MAIN LOOP
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

                # TOGGLE PAUSE
                elif event.key == pygame.K_p:
                    if game_state == "playing":
                        game_state = "paused"
                    elif game_state == "paused":
                        game_state = "playing"

                # RESTART
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

                # ANIMATED NAVICOMPUTER MESSAGE
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

                # CLEAR OLD OBJECTS
                planets.empty()
                blackholes.empty()
                wormholes.empty()

                # GENERATE NEW SECTOR CONTENT
                sector = world.generate_sector()

                for _ in range(sector.get("planet", 0)):
                    Planet(
                        random.randint(100, SCREEN_WIDTH - 100),
                        random.randint(100, SCREEN_HEIGHT - 100)
                    )

                for _ in range(sector.get("blackhole", 0)):
                    BlackHole(
                        random.randint(100, SCREEN_WIDTH - 100),
                        random.randint(100, SCREEN_HEIGHT - 100)
                    )

                for _ in range(sector.get("wormhole", 0)):
                    WormHole(
                        random.randint(100, SCREEN_WIDTH - 100),
                        random.randint(100, SCREEN_HEIGHT - 100)
                    )

            # DRAW GAME WORLD
            for obj in drawable:
                obj.draw(screen)

            # RESOURCE COLLECTION
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

            # BLACK HOLE EFFECTS
            for bh in blackholes:

                dist = player.position.distance_to(bh.position)

                if dist < bh.radius * 2:

                    direction = bh.position - player.position

                    if direction.length() > 0:
                        direction.normalize_ip()
                        player.position += direction * 120 * dt
                        player.radius *= 0.995

                # GAME OVER
                if dist < 10:
                    game_state = "game_over"

            # WORMHOLE TELEPORT
            for w in wormholes:

                if player.position.distance_to(w.position) < 40:

                    new_row = random.randint(0, GRID_SIZE - 1)
                    new_col = random.randint(0, GRID_SIZE - 1)

                    world.get_sector(new_row, new_col)

                    # REGENERATE SECTOR AFTER TELEPORT
                    planets.empty()
                    blackholes.empty()
                    wormholes.empty()

                    sector = world.generate_sector()

                    for _ in range(sector.get("planet", 0)):
                        Planet(random.randint(100, SCREEN_WIDTH - 100),
                            random.randint(100, SCREEN_HEIGHT - 100))

                    for _ in range(sector.get("blackhole", 0)):
                        BlackHole(random.randint(100, SCREEN_WIDTH - 100),
                                random.randint(100, SCREEN_HEIGHT - 100))

                    for _ in range(sector.get("wormhole", 0)):
                        WormHole(random.randint(100, SCREEN_WIDTH - 100),
                                random.randint(100, SCREEN_HEIGHT - 100))

                    # RESET PLAYER POSITION
                    player.position.x = SCREEN_WIDTH / 2
                    player.position.y = SCREEN_HEIGHT / 2

                    break  # PREVENT MULTIPLE TRIGGERS

            # DISPLAY SCORE
            score_text = font_ui.render(f"Resources: {score}", True, "white")
            screen.blit(score_text, (20, 20)) 

        # -------------------------------------------------
        # STATE: PAUSED (SHOW MINIMAP)
        # -------------------------------------------------
        elif game_state == "paused":

            # DRAW FROZEN WORLD
            for obj in drawable:
                obj.draw(screen)

            # OVERLAY MINIMAP
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

        #HIGHLIGHT PATH
        if square in path:
            pygame.draw.rect(screen, "blue", rect)

        # DRAW GRID
        pygame.draw.rect(screen, "gray", rect, 1)

    # HIGHLIGHT PLAYER SECTOR
    if highlight_current:

        row, col = world.get_sector()   # ROW FIRST, COL SECOND

        rect = pygame.Rect(
            offset_x + col * cell_size,
            offset_y + row * cell_size,
            cell_size,
            cell_size
        )

        pygame.draw.rect(screen, "red", rect, 3)

# RUN MAIN ONLY IF FILE EXECUTRED DIRECTLY
if __name__ == "__main__":
    main()