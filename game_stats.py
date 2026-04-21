"""
game_stats.py
Lance Thongsavanh
This file holds the status of the game
4/14/2026
"""

# from pathlib import Path
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats():
    """This class handles the overall stats for the game
    """

    def __init__(self, game: "AlienInvasion") -> None:
        """Initializes variables based on the game

        Args:
            game (AlienInvasion): the current game
        """
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self):
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat.__sizeof__() > 20:
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.high_score = scores.get("high_score", 0)
        else:
            self.high_score = 0
            self.save_scores()

    def save_scores(self) -> None:
        scores = {
            "high_score": self.high_score
        }
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f"File Not Found: {e}")

    def reset_stats(self) -> None:
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1

    def update(self, colliisions) -> None:
        # update score
        self._update_score(colliisions)

        # update max_score
        self._update_max_score()
    
        # update high_score
        self._update_high_score()


    def _update_score(self, colliisions) -> None:
        for alien in colliisions.values():
            self.score += self.settings.alien_points
        #print(f"Basic: {self.score}")
    
    def _update_max_score(self) -> None:
        if self.score > self.max_score:
            self.max_score = self.score
        #print(f"Max: {self.max_score}")

    def _update_high_score(self) -> None:
        if self.score > self.high_score:
            self.high_score = self.score
        #print(f"High: {self.high_score}")

    def update_level(self) -> None:
        self.level += 1
        #print(self.level)