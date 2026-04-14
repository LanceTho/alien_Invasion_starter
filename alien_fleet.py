"""
alien_fleet.py
Lance Thongsavanh
This is the file for the Alien Fleet
4/14/2026
"""

import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:
    """This class handles the creation of the Aliens for the game
    """

    def __init__(self, game: "AlienInvasion") -> None:
        """Initializes variables based on the game

        Args:
            game (AlienInvasion): the current game
        """
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        self.create_fleet()

    def create_fleet(self) -> None:
        """Creates the fleet at the top half of the screen
        """
        alien_width = self.settings.alien_width
        alien_height = self.settings.alien_height
        screen_width = self.settings.screen_width
        screen_height = self.settings.screen_height

        fleet_width, fleet_height = self.calculate_fleet_size(alien_width, screen_width, alien_height, screen_height)
        
        x_offset, y_offset = self.calculate_offsets(alien_width, alien_height, screen_width, fleet_width, fleet_height)

        self._create_rectangle_fleet(alien_width, alien_height, fleet_width, fleet_height, x_offset, y_offset)

    def _create_rectangle_fleet(self, alien_width: int, alien_height: int, fleet_width: int, fleet_height: int, x_offset: int, y_offset: int) -> None:
        """Creates the fleet in a rectangle shape

        Args:
            alien_width (int): width of the Alien sprite
            alien_height (int): height of the Alien sprite
            fleet_width (int): width of the Fleet
            fleet_height (int): height of the Fleet
            x_offset (int): offset for the x-value
            y_offset (int): offset for the y-value
        """
        for row in range(fleet_height):
            for col in range(fleet_width):
                current_x = alien_width * col + x_offset
                current_y = alien_height * row + y_offset
                if col % 2 == 0 or row % 2 == 0:
                    continue
                self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_width: int, alien_height: int, screen_width: int, fleet_width: int, fleet_height: int) -> tuple:
        """Finds the offsets for the x and y values

        Args:
            alien_width (int): width of the Alien sprite
            alien_height (int): height of the Alien sprite
            screen_width (int): width of the screen
            fleet_width (int): width of the Fleet
            fleet_height (int): height of the Fleet

        Returns:
            tuple: the x offset value and y offset value
        """
        half_screen = self.settings.screen_height//2
        fleet_horizontal_space = fleet_width * alien_width
        fleet_vertical_space = fleet_height * alien_height
        x_offset = int((screen_width - fleet_horizontal_space)//2)
        y_offset = int((half_screen-fleet_vertical_space)//2)
        return x_offset,y_offset

    def calculate_fleet_size(self, alien_width: int, screen_width: int, alien_height: int, screen_height: int) -> tuple:
        """Calculates the width and height of the Fleet

        Args:
            alien_width (int): width of the Alien sprite
            screen_width (int): width of the screen
            alien_height (int): height of the Alien sprite
            screen_height (int): height of the screen

        Returns:
            tuple: width of the Fleet and the height of the Fleet
        """
        fleet_width = (screen_width//alien_width)
        fleet_height = ((screen_height / 2)//alien_height)

        if fleet_width % 2 == 0:
            fleet_width -= 1
        else:
            fleet_width -= 2

        if fleet_height % 2 == 0:
            fleet_height -= 1
        else:
            fleet_height -= 2

        return int(fleet_width), int(fleet_height)
    
    def _create_alien(self, current_x: int, current_y: int) -> None:
        """Creates an Alien and adds it to the fleet

        Args:
            current_x (int): x-position
            current_y (int): y-position
        """
        new_alien = Alien(self, current_x, current_y)

        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """Checks if the fleet hits the edge of the screen
        """
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break

    def _drop_alien_fleet(self) -> None:
        """Moves the fleet down
        """
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed
            
    def update_fleet(self) -> None:
        """Updates the fleet
        """
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self) -> None:
        """Draws the fleet of Aliens
        """
        alien: "Alien"
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group):
        """Checks if the fleet collided with another group

        Args:
            other_group (_type_): the other objects it can interact with

        Returns:
            dict: updated fleet
        """
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    
    def check_fleet_bottom(self) -> bool:
        """Checks if the fleet reached the bottom of the screen

        Returns:
            bool: Returns true if it did, otherwise returns false
        """
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_height:
                return True
        return False
    
    def check_destroyed_status(self):
        """Checks if all of the aliens in the fleet are destroyed

        Returns:
            bool: the current status of the fleet
        """
        return not self.fleet