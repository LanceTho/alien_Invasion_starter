"""
alien.py
Lance Thongsavanh
This file has the Alien class
4/9/2026
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Alien(Sprite):
    """This class handles the ship's shooting

    Args:
        Sprite (_type_): _description_
    """
    
    def __init__(self, game: "AlienInvasion", x: float, y: float) -> None:
        """Initializes variables based on the game

        Args:
            game (AlienInvasion): the current game
        """
        super().__init__()
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, (self.settings.alien_width, self.settings.alien_height))

        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)
        
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self) -> None:
        """Moves the alein
        """
        temp_speed = self.settings.fleet_speed
        self.x += temp_speed
        self.rect.x = self.x

    def draw_alien(self) -> None:
        """Displays the alien
        """
        self.screen.blit(self.image, self.rect)

    