import curses
from typing import List, Tuple

from enums import COLORS

SIMULATION_SPEED: int = 5
TRAFFIC_LIGHT_WAIT_TIME: float = 20 / SIMULATION_SPEED
URGENCY_GAP = 3

MAP_FILE: str = "maps/small_sample.txt"

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
city = curses.newwin(100, 40, 0, 0)
console = curses.newwin(20, 100, 0, 40)
console.scrollok(True)
console.idlok(True)

curses.start_color()

curses.init_pair(COLORS.RED.value, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(COLORS.YELLOW.value, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(COLORS.GREEN.value, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(COLORS.BLUE.value, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(COLORS.WHITE.value, curses.COLOR_WHITE, curses.COLOR_BLACK)

curses.curs_set(0)

