import pygame

class BlackHole(pygame.sprite.Sprite):

    containers = ()

    def __init__(self,x,y,radius=60):
        super().__init__(self.containers)

        self.position = pygame.Vector2(x,y)
        self.radius = radius


    def update(self,dt,player):

        dist = player.position.distance_to(self.position)

        if dist < self.radius*2:

            direction = self.position - player.position

            if direction.length() > 0:

                direction.normalize_ip()
                player.position += direction * 120 * dt
                player.radius *= 0.995


    def draw(self,screen):

        pygame.draw.circle(screen,"purple",self.position,self.radius,1)
