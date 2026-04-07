import random
from planet import Planet
from blackhole import BlackHole
from wormhole import WormHole
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def load_sector(world, visited_sectors):
    key = world.get_sector()
                    
    if key not in visited_sectors:

        sector_data = {
            "planets": [],
            "blackholes": [],
            "wormholes": []
        }

        sector_counts = world.generate_sector()

        for _ in range(sector_counts.get("planet", 0)):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 100)
            planet = Planet(x, y)
            sector_data["planets"].append({
                "x": x,
                "y": y,
                "resources": planet.resources
            })

            planet.kill()  # remove temporary instance

        for _ in range(sector_counts.get("blackhole", 0)):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 100)
            sector_data["blackholes"].append((x, y))

        for _ in range(sector_counts.get("wormhole", 0)):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 100)
            sector_data["wormholes"].append((x, y))

        visited_sectors[key] = sector_data

    return visited_sectors[key]