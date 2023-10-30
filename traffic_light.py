import asyncio
from typing import List, Tuple
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from config import SIMULATION_SPEED, COLORS

class TrafficLightAgent(Agent):
    def __init__(self, jid, password, environment):
        super().__init__(jid, password)
        self.environment = environment

    class behave(CyclicBehaviour):
        position: List[int]
        ligth: COLORS
        name: str

        def get_character(self) -> Tuple[str, COLORS]:
            return ("l", self.light)

        def get_name(self) -> str:
            return self.name
        
        async def on_start(self):
            self.name = self.agent.name
            self.environment = self.agent.environment
            self.light = COLORS.RED

        async def response(self, message: Message, timeout: float):
            reply = message.make_reply()
            reply.set_metadata("performative", "inform")
            reply.set_metadata("timeout", str(timeout))
            await self.send(reply)

        async def run(self):

            msg = await self.receive(5 / SIMULATION_SPEED) 
            if msg:
                await self.response(msg, 5 / SIMULATION_SPEED)
            self.light = COLORS.GREEN
            self.environment.print_city()

            msg = await self.receive(5 / SIMULATION_SPEED) 
            if msg:
                await self.response(msg, 0)
            self.light = COLORS.YELLOW
            self.environment.print_city()

            msg = await self.receive(1 / SIMULATION_SPEED) 
            if msg:
                await self.response(msg, 0)
            self.light = COLORS.RED
            self.environment.print_city()

    async def setup(self):
        self.my_behav = self.behave()
        self.add_behaviour(self.my_behav)
