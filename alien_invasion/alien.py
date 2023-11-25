from typing import Any
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """class for aliens so we got what to pew pew"""

    def __init__(self,ai_game):
        """initialize alien"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
    
    def check_edges(self):
        """return true if alien hits edge of screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= screen_rect.left)

    def update(self):
        """move alien to the right"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x