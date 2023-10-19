import asyncio
import random
import math
from typing import List
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from config import SIMULATION_SPEED, DIRECTIONS
from environment import TYPE, Environment

class CarAgent(Agent):

    def __init__(self, jid, password, environment: Environment):
        super().__init__(jid, password)
        self.environment = environment
        self.position = [2, 0]
        self.direction = DIRECTIONS.EAST

    class behave(CyclicBehaviour):
        position: List[int]
        direction: DIRECTIONS
        name: str
        environment: Environment
        stop: bool = False

        def get_position(self):
            return self.position

        def get_name(self):
            return self.name

        async def on_start(self):
            self.position = self.agent.position
            self.name = self.agent.name
            self.environment = self.agent.environment
            self.direction = self.agent.direction

        async def run(self):

            directions = self.environment.get_possible_directions(position=self.position, direction=self.direction)

            if len(directions) == 1:
                self.direction = directions[0]
            elif len(directions) > 1:
                self.direction = random.choice(directions)
            print(self.direction)

            new_position = self.position
            new_position[0] += -1 * int(math.sin(math.radians(self.direction.value)))
            new_position[1] += int(math.cos(math.radians(self.direction.value)))

            self.position = new_position
        

            self.environment.update_city(name=self.name, position=self.position)
            await asyncio.sleep(1 / SIMULATION_SPEED)

    async def setup(self):
        self.my_behav = self.behave()
        self.add_behaviour(self.my_behav)
