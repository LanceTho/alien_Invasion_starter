"""
ship.py
Lance Thongsavanh
This file has the Ship class
4/9/2026
"""

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal


class Ship():
    """This class handles the ship that the player controls
    """
    
    def __init__(self, game: "AlienInvasion", arsenal: "Arsenal") -> None:
        """Initializes variables based on the game and arsenal

        Args:
            game (AlienInvasion): The current game
            arsenal (Arsenal): The ship's loadout
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, (self.settings.ship_width, self.settings.ship_height))

        self.rect = self.image.get_rect()
        self._center_ship()

        self.moving_right = False
        self.moving_left = False
        self.arsenal = arsenal

    def _center_ship(self) -> None:
        self.rect.midbottom = self.boundaries.midbottom
        self.x = self.rect.x

    def update(self) -> None:
        """Updates the ship's position
        """
        # updating position of the ship
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self) -> None:
        """Moves the ship left or right if it's still within the boundaries of the screen
        """
        temp_speed = self.settings.ship_speed
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed

        self.rect.x = self.x

    def draw(self) -> None:
        """Draws the ship
        """
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self) -> bool:
        """Calls the fire_bullet function from the Arsenal class

        Returns:
            bool: True if it did fire and False if it didn't
        """
        return self.arsenal.fire_bullet()
    
    def check_collisions(self, other_group) -> bool:
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False
