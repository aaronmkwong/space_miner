import pygame

# base class for game objects
# extends sprite class to also store a position, velocity, radius
# player is triangle with non-visible circle to detect collisions

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass
    
    # check for collision where distance from centre is less than  radius sum
    def collision(self,CircleShape):
        if self.position.distance_to(CircleShape.position) < (self.radius + CircleShape.radius):
            return True
        else:
            return False
