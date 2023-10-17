from typing import List
import curses

CITY_HEIGHT = 24
CITY_WIDTH = 24

from enum import Enum

class TYPE(Enum):
    EMPTY = "-"
    CAR = "*"
    LIGHT = "+"

#class Environment(Agent):
#    class behave(CyclicBehaviour):
#        
#        city = [[0 for i in range(CITY_WIDTH)] for j in range(CITY_HEIGHT)]
#
#        # async def on_start(self):
#
#        async def run(self):
#            await asyncio.sleep(1)
#
#        async def on_end(self):
#            print("Behaviour finished with exit code {}.".format(self.exit_code))
#
#    async def setup(self):
#        print("Agent starting . . .")
#        self.my_behav = self.behave()
#        self.add_behaviour(self.my_behav)

class Environment:

    city = [[[] for i in range(CITY_WIDTH)] for j in range(CITY_HEIGHT)]
    stdscr = curses.initscr()
    
    def get_position(self, position: List[int]):
        return self.city[position[0]][position[1]]

    def get_from_position(self, position: List[int]):
        return self.city[position[0]][position[1]]

    def update_city(self, component):
        position = component.get_position()
        name = component.get_name()

        for i in range(CITY_WIDTH):
            for j in range(CITY_HEIGHT):
                if (self.city[i][j] == []): continue
                if (self.city[i][j].get_name() == name): self.city[i][j] = []

        self.city[position[0]][position[1]] = component
        self.print_city()

    def print_city(self):
        self.stdscr.clear()
        for i in range(CITY_WIDTH):
            for j in range(CITY_HEIGHT):
                self.stdscr.addstr("{char} ".format(char = self.city[i][j].get_type().value) if self.city[i][j] else "- ")
            self.stdscr.addch("\n")
        print("", end="\r")
        self.stdscr.refresh()







