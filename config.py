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

MAP_FILE = "maps/city.txt"

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
cursor.hide()
