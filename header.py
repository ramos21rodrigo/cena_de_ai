import curses
from enum import Enum

TRAFFIC_LIGHT_WAIT_TIME = 10 
DAY_DURATION = 60

class ACTIONS(Enum):
    STOP = "1"
    PASS = "2"
    ALLOW = "3"
    DENY = "4"
    CHANGE_COLOR = "5"
    ASK_FOR_ACTION = "6"
    CONNECT = "7"
    UPDATE_SPEED = "8"

class COLORS(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3
    WHITE = 4
    GRAY = 5

class DIRECTIONS(Enum):
    EAST = 0
    NORTH = 90
    WEST = 180
    SOUTH = 270

class TYPE(Enum):
    ROAD = " "
    LIGHT = "+"
    WALL = "#"

stdscr = curses.initscr()
city = curses.newwin(100, 30, 0, 0)

logs = curses.newwin(100, 25, 0, 30)
logs.scrollok(True)
logs.idlok(True)

curses.start_color()
curses.curs_set(0)
curses.init_pair(COLORS.RED.value, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(COLORS.YELLOW.value, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(COLORS.GREEN.value, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(COLORS.WHITE.value, curses.COLOR_WHITE, curses.COLOR_BLACK)



