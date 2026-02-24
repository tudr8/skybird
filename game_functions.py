# Refactoring Game code, (split the definations and code functions:)

import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


# Define Refactoring events: [split_the_functions:]
def check_keydown_events(event, settings, screen, ship, bullet):
    "Respond to the keyboard user press"            
    
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True 
    
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullet)
     # Quit 'q' users keypress:
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    "Respond to the key Releases"
    #elif event.type == pygame.KEYUP:
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False    
    elif event.key == pygame.K_LEFT:
          ship.moving_left = False
   
# Create defination for keys pressing and mouse:


def check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start new game when the player click play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
       # Resetting the game settings:
        settings.initialize_dynamic_settings()
       # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
      
    
        # Reset the game statistics:
        stats.reset_stats()
        stats.game_active = True
        # Reset the scoreboard image. 
        sb.prep_score() 
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        #Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        #Create a new fleet and center the ship.
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

def fire_bullet(settings, screen, ship, bullet):
    "Fire bullets in limits"
    # Create a new bullet and add it to the bullet Group: 
    if len(bullet) < settings.bullet_allowed:
           new_bullet = Bullet(settings, screen, ship, bullet)
           bullet.add(new_bullet)
 



def check_events(ship, aliens, settings, screen, bullets, stats, sb, play_button):
    "resonding to keyboard pressing and mouse events"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship) 
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)



def get_number_aliens_x(settings, alien_width):
    """Determine the numbers of aliens in rows"""
    available_space_x = settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / ( 2 * alien_width))
    return number_alien_x

def get_number_rows(settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in row"""
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def create_fleet(settings, screen, ship, aliens):
    """Create full fleet of aliens"""
  
    alien = Alien(settings, screen)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)
    
    
    for row_number in range(number_rows):
       for alien_number in range (number_aliens_x):
           create_alien(settings, screen, aliens, alien_number, row_number)
           alien = Alien(settings, screen)
           aliens.add(alien)


def update_bullets(settings, screen, stats, sb, ship, aliens, bullets):
    "Update the position of the bullets and git rid of old bullets, [ Avoid consuming Memory]"
     # Get rid of bullet dissapeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(settings, screen, stats, sb, ship, aliens, bullets)
    
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(settings, screen, ship, aliens)
    
    bullets.update()
    

def check_high_score(stats, sb):
    """Check to see if there is a high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collision(settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet_aliens collision"""
    # Remove any aliens or bullet that is collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        bullets.empty()
        settings.increase_speed()
        # Increasing level.
        stats.level += 1
        sb.prep_level()
        
        create_fleet(settings, screen, ship, aliens)
   
    

def check_fleet_edges(settings, aliens):
    """Response appropairty if aliens reached to edges."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break

def change_fleet_direction(settings, aliens):
    """Drop the entrie fleet and changes the fleet direction."""
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction*= -1

def ship_hit(settings, stats, sb, screen, ship, aliens, bullets):
    """Responding to ship being hit by alien"""
    if stats.ships_left > 0:
    # Decrement ship left
       stats.ship_left -= 1
    
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        
        # Update scoreboard.
        sb.prep_ships()  
    
    # Empty the list of aliens and bullets:
        aliens.empty()
        bullets.empty()

    # Create a new fleet and center the ship:
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()  
 
    # Pause:
        sleep(0.5) 
   

def check_aliens_bottom(settings, stats, sb, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
           # Treat this the same as if the ship got hit:
            ship_hit(settings, stats, sb, screen, ship, aliens, bullets)
            break 

def update_aliens(settings, stats, sb,  screen, ship, aliens, bullets):
    """
    Check if the fleet on the edge
    Update the position of all aliens in the fleet.
    """
    check_fleet_edges(settings, aliens)
    aliens.update()
    
    # Look for alien ship collisions:
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, sb, screen, ship, aliens, bullets)
        print("Ship hit!!!")
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(settings, stats, sb, screen, ship, aliens, bullets) 



# Create defination for game screen settings and updating:
def update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button):
    "Update the images on the screen , flip to the new screen"
    screen.fill(settings.bg_color)
    
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    ship.blitme()
    aliens.draw(screen)
    # Draw the score information.
    sb.show_score()
    
    # Draw the play button if the game inactive.
    if not stats.game_active:
       play_button.draw_button()
    
    #Make the most recently drawn screen visible:
    pygame.display.flip()  

