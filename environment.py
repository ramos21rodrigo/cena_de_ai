from typing import List
import os
import math
import curses
import cursor

from config import DIRECTIONS

MAP_FILE = "maps/city.txt"

from enum import Enum

class TYPE(Enum):
    ROAD = "."
    WALL = "-"
    LIGHT = "+"

class Environment:

    city_schema: List[List[TYPE]]
    city: List[List[str]]
    city_height: int
    city_width: int

    def __init__(self):

        cursor.hide()

        file = open(MAP_FILE, "r")
        content = file.readlines()

        self.city_height = len(content)
        self.city_width = len(content[0]) - 1
        self.city_schema = [[TYPE.ROAD for i in range(self.city_width)] for j in range(self.city_height)]
        self.city = [["" for i in range(self.city_width)] for j in range(self.city_height)]
        
        for i in range(self.city_height):
            for j in range(self.city_width):
                self.city_schema[i][j] = TYPE(content[i][j])

        self.stdscr = curses.initscr()
        curses.endwin()

    def get_position(self, position: List[int]):
        return self.city[position[0]][position[1]]

    def check_pattern(self, position: List[int], angle: int, line_to_check: int = 1) -> bool:
        
        angle_radians: float = math.radians(angle)

        delta_row: int = -round(math.sin(angle_radians))
        delta_col: int = round(math.cos(angle_radians))

        new_row: int = position[0] + delta_row * line_to_check
        new_col: int = position[1] + delta_col * line_to_check

        return self.city_schema[new_row + delta_col][new_col - delta_row] == TYPE.WALL and self.city_schema[new_row][new_col] != TYPE.WALL and self.city_schema[new_row - delta_col][new_col + delta_row] != TYPE.WALL and self.city_schema[new_row - delta_col * 2][new_col + delta_row * 2] == TYPE.WALL

    
    def get_possible_directions(self, position: List[int], direction: DIRECTIONS) -> List[DIRECTIONS]:
        to_left: int = direction.value + 90 if direction.value + 90 < 360 else 0 + direction.value - 90
        to_right: int = direction.value - 90 if direction.value - 90 >= 0 else 360 + direction.value - 90
        directions = []
        if (self.check_pattern(position, direction.value, 2)):
            directions.append(DIRECTIONS(direction.value))
        if (self.check_pattern(position, to_right)):
            directions.append(DIRECTIONS(to_right))
        if (self.check_pattern(position, to_left, 2)):
            directions.append(DIRECTIONS(to_left))

        return directions


    def update_city(self, name:str, position: List[int]):
        for i in range(self.city_height):
            for j in range(self.city_width):
                if (self.city[i][j] == ""): continue
                if (self.city[i][j] == name): 
                    self.city[i][j] = ""
                    break

        self.city[position[0]][position[1]] = name
        self.print_city()

    def print_city(self):
        os.system("clear")

        for i in range(self.city_height):
            for j in range(self.city_width):
                if self.city[i][j] != "": 
                    print("*", end="")
                else:
                    #print(j, end="")
                    print(self.city_schema[i][j].value, end="")
            print()



 

