import asyncio
from typing import List
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from config import SIMULATION_SPEED, DIRECTIONS, environment
from environment import TYPE

class CarAgent(Agent):

    def __init__(self, jid, password, position: List[int], direction: DIRECTIONS):
        super().__init__(jid, password)
        self.set("position", position)
        self.set("direction", direction)
        self.set("name", self.name)

    class behave(CyclicBehaviour):
        position: List[int]
        direction: DIRECTIONS
        name: str

        def get_position(self):
            return self.position

        def get_type(self):
            return TYPE.CAR

        def get_name(self):
            return self.name

        async def on_start(self):
            self.position = self.get("position")
            self.direction = self.get("direction")
            self.name = self.get("name")

        async def run(self):
            self.position[0] += self.direction.value[0]
            self.position[1] += self.direction.value[1]

            self.kill(exit_code = 0)

            environment.update_city(self)
            await asyncio.sleep(1 / SIMULATION_SPEED)

    async def setup(self):
        self.my_behav = self.behave()
        self.add_behaviour(self.my_behav)
