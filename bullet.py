"""
bullet.py
Lance Thongsavanh
This file has the Bullet class
4/9/2026
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    """This class handles the ship's shooting

    Args:
        Sprite (_type_): _description_
    """
    
    def __init__(self, game: "AlienInvasion") -> None:
        """Initializes variables based on the game

        Args:
            game (AlienInvasion): the current game
        """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_width, self.settings.bullet_height))

        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y = self.rect.y

    def update(self) -> None:
        """Moves the position of the bullet by a set speed
        """
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self) -> None:
        """Displays the bullet
        """
        self.screen.blit(self.image, self.rect)