from enum import Enum

class DIRECTIONS(Enum):
    NONE = -1
    EAST = 0
    NORTH = 90
    WEST = 180
    SOUTH = 270

class COLORS(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3

class ACTIONS(Enum):
    STOP = "stop"
    PASS = "pass"

class TYPE(Enum):
    ROAD = " "
    LIGHT = "+"
    WALL = "#"

