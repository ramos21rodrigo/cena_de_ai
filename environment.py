from typing import List
import time
import math
import curses

from config import DIRECTIONS

CITY_HEIGHT = 6
CITY_WIDTH = 12

from enum import Enum

class TYPE(Enum):
    ROAD = "."
    WALL = "-"
    LIGHT = "+"

class Environment:

    city_schema = [
            ['-','-','-','-','-','-','-','-','-','-','-','-'],
            ['.','.','.','.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.','.','.','.'],
            ['-','-','-','-','-','-','-','.','-','-','-','-'],
            ['-','-','-','-','-','-','-','.','-','-','-','-'],
            ['-','-','-','-','-','-','-','-','-','-','-','-']
            ]
    city = [["" for i in range(CITY_WIDTH)] for j in range(CITY_HEIGHT)]
    stdscr = curses.initscr()

    def get_position(self, position: List[int]):
        return self.city[position[0]][position[1]]

    def get_possible_directions(self, position: List[int], direction: DIRECTIONS) -> List[DIRECTIONS]:
        #to_left: int = direction.value + 90 if direction.value + 90 < 360 else 0
        to_right: int = direction.value - 90 if direction.value - 90 > 0 else 360 + direction.value - 90
        directions = []
        if (self.city_schema[position[0] + -1 * int(math.sin(math.radians(to_right)))][position[1] + int(math.cos(math.radians(to_right)))] != TYPE.WALL.value):
            directions.append(DIRECTIONS(to_right))

        return directions



    def update_city(self, name:str, position: List[int]):
        for i in range(CITY_HEIGHT):
            for j in range(CITY_WIDTH):
                if (self.city[i][j] == ""): continue
                if (self.city[i][j] == name): 
                    self.city[i][j] = ""
                    break

        self.city[position[0]][position[1]] = name
        self.print_city()


    def print_city(self):
        self.stdscr.clear()
        for i in range(CITY_HEIGHT):
            for j in range(CITY_WIDTH):
                if (self.city[i][j]): self.stdscr.addstr("*")
                else: self.stdscr.addstr(self.city_schema[i][j])
            self.stdscr.addch("\n")
        print("", end="\r")
        self.stdscr.refresh()







