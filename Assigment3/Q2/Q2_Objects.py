from dataclasses import dataclass


@dataclass
class Player:
    name: str
    wins: int
    losses: int
    ties: int

    @property
    def games(self):
        return self.wins + self.losses + self.ties
