import asyncio
from typing import List
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from config import SIMULATION_SPEED, DIRECTIONS, environment

class CarAgent(Agent):

    def __init__(self, jid, password, position: List[int], direction: DIRECTIONS):
        super().__init__(jid, password)
        self.set("position", position)
        self.set("direction", direction)

    class behave(CyclicBehaviour):
        position: List[int]
        direction: DIRECTIONS

        async def on_start(self):
            self.position = self.get("position")
            self.direction = self.get("direction")

        async def run(self):
            self.position[0] += self.direction.value[0]
            self.position[1] += self.direction.value[1]
            environment.update_city(position = self.position)
            await asyncio.sleep(1 / SIMULATION_SPEED)

    async def setup(self):
        self.my_behav = self.behave()
        self.add_behaviour(self.my_behav)
