import asyncio
from typing import List
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import os

CITY_HEIGHT = 24
CITY_WIDTH = 24

from enum import Enum, auto

class SPACE(Enum):
    EMPTY = auto()
    CAR = auto()
    LIGHT = auto()


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

    city = [[0 for i in range(CITY_WIDTH)] for j in range(CITY_HEIGHT)]
    
    def get_position(self, position: List[int]):
        block = self.city[position[0]][position[1]]

    def update_city(self, position: List[int]):
        self.city[position[0]][position[1]] = 1
        self.print_city()

    def print_city(self):
        os.system("clear")

        for i in range(CITY_WIDTH):
            for j in range(CITY_HEIGHT):
                print(self.city[i][j], end=" ")
            print()







