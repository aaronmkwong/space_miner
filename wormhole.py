import pygame
import random

class WormHole(pygame.sprite.Sprite):

    containers = ()

    def __init__(self,x,y):
        super().__init__(self.containers)

        self.position = pygame.Vector2(x,y)


    def draw(self,screen):

        pygame.draw.ellipse(
            screen,
            "cyan",
            (self.position.x-40,self.position.y-70,80,140),
            2
        )
