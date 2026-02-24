### Creatig game state class: ##
class GameStats():
    """Track static for Alien Invasion"""
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        # Start alien invasion in an active stats:
        self.game_active = False
        # High score should never be reset:
        self.high_score = 0
    
    
    def reset_stats(self):
        """Initialize statics that can change during the game""" 
        self.ship_left = self.settings.ship_limit 
        self.score = 0
        self.level = 1
