from typing import List, Tuple, Union
import math
import curses
from car import CarAgent

from config import DIRECTIONS, MAP_FILE, traffic_agents, stdscr

from enum import Enum

from traffic_light import TrafficLightAgent

class TYPE(Enum):
    ROAD = " "
    LIGHT = "+"
    WALL = "-"

class Environment:
    city_schema: List[List[Union[TrafficLightAgent, TYPE]]]
    city: List[List[Union[CarAgent, None]]]
    city_height: int
    city_width: int

    async def create_city(self) -> None:
        file = open(MAP_FILE, "r")
        content = file.readlines()

        self.city_height = len(content)
        self.city_width = len(content[0]) - 1
        self.city_schema = [[TYPE.ROAD for i in range(self.city_width)] for j in range(self.city_height)]
        self.city = [[None for i in range(self.city_width)] for j in range(self.city_height)]
        
        for i in range(self.city_height):
            for j in range(self.city_width):
                if (content[i][j] == TYPE.LIGHT.value):
                    traffic = traffic_agents.pop(0)
                    agent = TrafficLightAgent(traffic[0], traffic[1], self)
                    await agent.start()
                    self.city_schema[i][j] = agent.my_behav
                    continue
                self.city_schema[i][j] = TYPE(content[i][j])

    # find pattern [ROAD, ROAD]
    #                   [line_to_check] (distance between pattern and CAR)
    #                      CAR
    #
    # from the angle [left, right, up] 
    # using the math.sin() and math.cos() functions
    def check_pattern(self, position: List[int], angle: int, line_to_check: int = 1) -> bool:
        angle_radians: float = math.radians(angle)

        delta_row: int = -round(math.sin(angle_radians))
        delta_col: int = round(math.cos(angle_radians))

        new_row: int = position[0] + delta_row * line_to_check
        new_col: int = position[1] + delta_col * line_to_check

        second_space: TYPE = self.city_schema[new_row][new_col]
        third_space: TYPE = self.city_schema[new_row - delta_col][new_col + delta_row]

        return second_space != TYPE.WALL and third_space != TYPE.WALL
    
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


    def get_position(self, position: List[int]) -> str:
        if isinstance(self.city_schema[position[0]][position[1]], TYPE): return ""
        return self.city_schema[position[0]][position[1]].get_name()
        if self.city[position[0]][position[1]] == None: return ""
        return self.city[position[0]][position[1]].get_name()


    def update_city(self, car: CarAgent):
        position: List[int] = car.get_position()
        name: str = car.get_name()

        for i in range(self.city_height):
            for j in range(self.city_width):
                if (self.city[i][j] == None): continue
                if (self.city[i][j].get_name() == name): 
                    self.city[i][j] = None
                    break

        self.city[position[0]][position[1]] = car
        self.print_city()

    def print_city(self):
        stdscr.clear()

        for i in range(self.city_height):
            for j in range(self.city_width):
                if self.city[i][j] is not None: 
                    stdscr.addch(self.city[i][j].get_arrow())
                    continue

                if not isinstance(self.city_schema[i][j], TYPE):
                    traffic: TrafficLightAgent = self.city_schema[i][j].get_character()
                    stdscr.addch(traffic[0], curses.color_pair(traffic[1].value))
                    continue

                stdscr.addch(self.city_schema[i][j].value)

            stdscr.addch('\n')
        stdscr.refresh()



 

