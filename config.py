import curses
from enum import Enum

class ACTIONS(Enum):
    STOP = 1
    PASS = 2
    ALLOW = 3
    DENY = 4
    CHANGE_COLOR = 5
    ASK_FOR_ACTION = 6

class COLORS(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    WHITE = 5
    GRAY = 6

class DIRECTIONS(Enum):
    EAST = 0
    NORTH = 90
    WEST = 180
    SOUTH = 270

class TYPE(Enum):
    ROAD = " "
    LIGHT = "+"
    WALL = "#"

FILE = "maps/small_sample.txt"
TRAFFIC_LIGHT_WAIT_TIME = 10 
DAY_DURATION = 60

disruption_agent = ("disruption@localhost", "disruption")

stdscr = curses.initscr()
city = curses.newwin(100, 100, 0, 0)
#city = curses.newwin(200, 200, 0, 0)
console = curses.newwin(50, 30, 0, 100)
#console = curses.newwin(20, 100, 0, 200)
console.scrollok(True)
console.idlok(True)

curses.start_color()

curses.init_pair(COLORS.RED.value, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(COLORS.YELLOW.value, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(COLORS.GREEN.value, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(COLORS.BLUE.value, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(COLORS.WHITE.value, curses.COLOR_WHITE, curses.COLOR_BLACK)

curses.curs_set(0)


