import curses
from typing import List, Tuple

from enums import COLORS

SIMULATION_SPEED: int = 15
TRAFFIC_LIGHT_WAIT_TIME: float = 20 / SIMULATION_SPEED
URGENCY_GAP: int = 3
DAY_DURATION: float = 60 / SIMULATION_SPEED #minute

MAP_FILE: str = "maps/big_sample.txt"

disruption_agent: Tuple[str, str] = ("disruption@localhost", "disruption")

traffic_agents: List[Tuple[str, str]] = [
        ("traffic@localhost", "traffic"),
        ("traffic1@localhost", "traffic"),
        ("traffic2@localhost", "traffic"),
        ("traffic3@localhost", "traffic"),
        ("traffic4@localhost", "traffic"),
        ("traffic5@localhost", "traffic"),
        ("traffic6@localhost", "traffic"),
        ("traffic7@localhost", "traffic"),
        ("traffic8@localhost", "traffic"),
        ("traffic9@localhost", "traffic"),
        ("traffic10@localhost", "traffic"),
        ("traffic11@localhost", "traffic"),
        ("traffic12@localhost", "traffic"),
        ("traffic13@localhost", "traffic"),
        ("traffic14@localhost", "traffic"),
        ("traffic15@localhost", "traffic"),
        ("traffic16@localhost", "traffic"),
        ("traffic17@localhost", "traffic"),
        ("traffic18@localhost", "traffic"),
        ("traffic19@localhost", "traffic"),
        ("traffic20@localhost", "traffic"),
        ]

stdscr = curses.initscr()
city = curses.newwin(100, 100, 0, 32)
clock = curses.newwin(1, 30, 0, 1)
console = curses.newwin(20, 30, 2, 1)
console.scrollok(True)
console.idlok(True)

curses.start_color()

curses.init_pair(COLORS.RED.value, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(COLORS.YELLOW.value, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(COLORS.GREEN.value, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(COLORS.BLUE.value, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(COLORS.WHITE.value, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(COLORS.GRAY.value, 242, curses.COLOR_BLACK)

curses.curs_set(0)

