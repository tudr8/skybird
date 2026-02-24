### Creating pygame window,size and resolutions, responding to the user input: ##

# Importing Alien game modules: ### Modules is created by [ *Registered* | **pygame_team** ] ###

import sys        
import pygame 
import game_functions as gf
from pygame.sprite import Group
from settings import Settings
from ship import Ship     
from alien import Alien
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard



def run_game():
    "Initialize the Game and create screen window"
    # The primary game instructions vaulues:
    pygame.init()
    # settings from class values.
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))   # TypeError: size must be two numbers.
    bg_color = (230, 230, 230)
    pygame.display.set_caption("Alien Invasion")
    
    # Make the play button:
    play_button = Button(settings, screen, "Play")
    
    # Create an instance to store game_statistics ship and aliens:
    stats = GameStats(settings)
    
    # Space ship values:
    ship = Ship(settings, screen)
    
    # Create a group bullets:
    bullets = Group()
    aliens = Group()   
   # Make an alien:
    alien = Alien(settings, screen)
   
   # Create a fleet of aliens: 
    gf.create_fleet(settings, screen, ship, aliens)
    
    # Create an instance for game score:
    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)

    
    # create a (main loop) for the game:
    while True:   
        gf.check_events(ship, aliens, settings, screen, bullets, stats, sb, play_button)
        if stats.game_active:
           ship.update()
        gf.update_bullets(settings, screen, stats, sb, ship, aliens, bullets)
        gf.update_aliens(settings, stats, sb, screen, ship, aliens, bullets)
        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button)
        
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
               
        
       
        # Determine, fill the screen color values:
        screen.fill(settings.bg_color) 
        ship.blitme()
        aliens.draw(screen)
        
        # Draw the play button if the game inactive.
        if not stats.game_active:
            play_button.draw_button()
        
        sb.show_score()
        # Make the recent screen is visible:
        pygame.display.flip()

run_game()                 


