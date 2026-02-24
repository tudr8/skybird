import pygame
from pygame.sprite import Sprite

# Create the Alien space ship class: 
class Ship(Sprite):
    def __init__(self, settings, screen):
        """Initialize the ship and the set of starting ship position."""
        super(Ship, self).__init__()
       # Create the Space ship defintion, Design, size, color, etc....: ###
        self.screen = screen 
        self.settings = settings
        # start, load the space ship image:
        self.image = pygame.image.load('images/ship.bmp')
        self.rect =  self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Create space ship starting position on the bottom of the screen:
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # Store the decimal value for the ship:
        self.center = float(self.rect.centerx)
        # Create the space ship movments:
        # Movement flag:
        self.moving_right = False
        self.moving_left = False
    
    def center_ship(self):
        """Center the ship on the screen."""
        self.centerx = self.screen_rect.centerx 
    
    
    def update(self):
        "Update the space ship position according to the movements flags"
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.ship_speed_factor
        
        # Update the rect object from self:    
        self.rect.centerx = self.center
    
    
  
    def blitme(self):
        "Draw the ship in the determined location"
        self.screen.blit(self.image, self.rect)

       
       
    