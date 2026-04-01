from circleshape import * 
from constants import *

# draw spaceship for player
# player looks like triangle but circle will represent hitbox

# inherit from CircleShape class
class Player(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0  
        self.timer = 0  
        self.radius = radius # current changing value, e.g. black hole shrinkage
        self.base_radius = radius # original constant value, e.g. escape black hole reset size
        self.color = "white"

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.triangle(), 2)

    # triangle for player 
    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = forward.rotate(90)

        tip = self.position + forward * self.radius
        left = self.position - forward * self.radius * 0.5 + right * self.radius * 0.5
        right_pt = self.position - forward * self.radius * 0.5 - right * self.radius * 0.5

        return [tip, left, right_pt]

    # player rotation
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    # player move
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    # apply keys 
    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_s]:
            self.move(dt)

        if keys[pygame.K_w]:
            self.move(-dt)
        
      


    
   





    
