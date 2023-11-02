import curses
import cursor
from enum import Enum
from typing import List, Tuple


SIMULATION_SPEED: int = 4

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

MAP_FILE = "maps/small_sample.txt"

traffic_agents: List[Tuple[str, str]] = [
        ("traffic@localhost", "traffic"),
        ("traffic1@localhost", "traffic"),
        ("traffic2@localhost", "traffic"),
        ("traffic3@localhost", "traffic"),
        ("traffic4@localhost", "traffic"),
        ("traffic5@localhost", "traffic"),
        ("traffic6@localhost", "traffic"),
        ]

stdscr = curses.initscr()
curses.start_color()

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

cursor.hide()
