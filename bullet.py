# import [*Registered_pygame*] modules to create Space ship bullets modules:

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    "Display and manage the bullets fired"
    def __init__(self, settings, screen, ship, bullets):
        super(Bullet, self).__init__()
        self.screen = screen 
        self.bullets = bullets
       
        # Create the Bullets rect:
        self.rect = pygame.Rect((0, 0, settings.bullet_width, settings.bullet_height))
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Bullet decimal values:
        self.y = float(self.rect.y)
        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        "Move the bullets up in a screen"
        # Update the decimal position:
        self.y -= self.speed_factor 
        #update the rect position:
        self.rect.y = self.y    

    def draw_bullet(self):
        "Draw the bullets on the screen"
        pygame.draw.rect(self.screen, self.color, self.rect)    