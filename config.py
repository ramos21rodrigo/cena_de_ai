import curses
from typing import List, Tuple

SIMULATION_SPEED: int = 5
TRAFFIC_LIGHT_WAIT_TIME: float = 20 / SIMULATION_SPEED

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
console = curses.newwin(100, 100, 0, 40)

curses.start_color()

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

curses.curs_set(0)

