from dataclasses import dataclass
import math


@dataclass
class RightTriangle:
    a: int = 0
    b: int = 0

    @property
    def c(self):  # calculates and returns the value for  side C
        return math.sqrt((self.a ** 2) + (self.b ** 2))
