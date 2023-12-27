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
    BLUE = 4
    WHITE = 5

class PERFORMATIVES(Enum):
    INFORM = "inform"
    REQUEST = "request"

class ACTIONS(Enum):
    STOP = "stop"
    PASS = "pass"
    ALLOW = "allow"
    DENY = "deny"
    CHANGE_COLOR = "change_color"
    ASK_FOR_ACTION = "ask_for_action"
    ONE_MORE_TO_QUEUE = "one_more_to_queue"
    USED = "used"

class TYPE(Enum):
    ROAD = " "
    LIGHT = "+"
    WALL = "#"

