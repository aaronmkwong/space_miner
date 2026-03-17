import pygame
import random

class Planet(pygame.sprite.Sprite):

    containers = ()

    def __init__(self, x, y, radius=80):
        super().__init__(self.containers)

        self.position = pygame.Vector2(x, y)
        self.radius = radius

        self.resources = []

        for _ in range(random.randint(10,20)):

            angle = random.uniform(0,6.28)
            dist = random.uniform(10,radius-10)

            rx = dist * pygame.math.Vector2(1,0).rotate_rad(angle).x
            ry = dist * pygame.math.Vector2(1,0).rotate_rad(angle).y

            self.resources.append([rx,ry,False])


    def draw(self,screen):

        pygame.draw.circle(screen,"green",self.position,self.radius,2)

        for r in self.resources:

            if not r[2]:

                pygame.draw.circle(
                    screen,
                    "yellow",
                    (self.position.x+r[0], self.position.y+r[1]),
                    3
                )
