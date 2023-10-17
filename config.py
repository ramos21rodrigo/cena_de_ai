from enum import Enum
from environment import Environment, TYPE

SIMULATION_SPEED: int = 2

class DIRECTIONS(Enum):
    NORTH = (1, 0)
    SOUTH = (-1, 0)
    EAST = (0, 1)
    WEST = (0, -1)

environment = Environment()
