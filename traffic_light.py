import asyncio
from typing import List
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from config import SIMULATION_SPEED, COLORS

class TrafficLightAgent(Agent):
    def __init__(self, jid, password, environment):
        super().__init__(jid, password)
        self.environment = environment

    class behave(CyclicBehaviour):
        position: List[int]
        ligth: COLORS

        def get_character(self) -> (chr, COLORS):
            return ("-", COLORS.RED)
        
        async def on_start(self):
            self.name = self.agent.name
            self.environment = self.agent.environment

        async def run(self):
            self.light = COLORS.GREEN
            print(self.light)
            await asyncio.sleep(10 / SIMULATION_SPEED)

            self.light = COLORS.YELLOW
            print(self.light)
            await asyncio.sleep(1 / SIMULATION_SPEED)

            self.light = COLORS.RED
            print(self.light)
            await asyncio.sleep(10 / SIMULATION_SPEED)

    async def setup(self):
        self.my_behav = self.behave()
        self.add_behaviour(self.my_behav)
