### Importing [*Registered_pygame*], Games Modules:
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
   """A class to represent a single alien"""
   def __init__(self, settings, screen):
      """Initialize the alien and it's starting position"""
      super(Alien, self).__init__()
      self.screen = screen
      self.settings = settings
      
      # load alien image and set the rect attributes:
      self.image = pygame.image.load('images/alien.bmp')
      self.rect = self.image.get_rect()
      
      # start the new alien on the top of the screen:
      self.rect.x = self.rect.width
      self.rect.y = self.rect.height
      self.x = int(self.rect.x)
      
      # store the alien exact position:
   
   def check_edges(self):
      """Return True if an alien on the edge of the screen"""
      screen_rect = self.screen.get_rect()
      if self.rect.right >= screen_rect.right:
         return True
      elif self.rect.left <= 0:
         return True
   
   
   def update(self):
      """Move the aliens to the right""" 
      
      self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)
      self.rect.x = self.x
   
   
   def blitme(self):
      # Draw the alien at the current location:
      self.screen.blit(self.image, self.rect)



  

