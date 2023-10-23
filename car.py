import asyncio
import random
import math
from typing import List
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from config import SIMULATION_SPEED, DIRECTIONS

class CarAgent(Agent):

    def __init__(self, jid, password, environment, position, direction):
        super().__init__(jid, password)
        self.position = position
        self.direction = direction
        self.environment = environment

    class behave(CyclicBehaviour):
        position: List[int]
        direction: DIRECTIONS
        name: str
        # environment: Environment avoid circular dependency
        stop: bool = False

        def get_position(self):
            return self.position

        def get_name(self):
            return self.name

        def get_arrow(self):
            if(self.direction == DIRECTIONS.NORTH):
                return "↑"
            if(self.direction == DIRECTIONS.SOUTH):
                return "↓"
            if(self.direction == DIRECTIONS.EAST):
                return "→"
            if(self.direction == DIRECTIONS.WEST):
                return "←"

        async def on_start(self):
            self.position = self.agent.position
            self.name = self.agent.name
            self.environment = self.agent.environment
            self.direction = self.agent.direction

        async def run(self):

            directions = self.environment.get_possible_directions(position=self.position, direction=self.direction)

            if len(directions) == 0:
                self.kill()
                return
            if len(directions) >= 1:
                self.direction = random.choice(directions)

            new_position = self.position
            new_position[0] -= round(math.sin(math.radians(self.direction.value)))
            new_position[1] += round(math.cos(math.radians(self.direction.value)))

            name = self.environment.get_position(position=new_position)
            #if (name != ""):
                   
            #else: 
            self.position = new_position
            self.environment.update_city(self)


            await asyncio.sleep(1 / SIMULATION_SPEED)

    async def setup(self):
        self.my_behav = self.behave()
        self.add_behaviour(self.my_behav)
