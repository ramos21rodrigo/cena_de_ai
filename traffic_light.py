import asyncio
from typing import List, Tuple
import time
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from config import SIMULATION_SPEED, COLORS, ACTIONS

class TrafficLightAgent(Agent):
    def __init__(self, jid: str, password: str, environment, horizontal: bool) -> None:
        super().__init__(jid, password)
        self.horizontal = horizontal
        self.environment = environment

    class behav(CyclicBehaviour):
        position: List[int]
        ligth: COLORS
        horizontal: bool
        name: str

        def get_character(self) -> Tuple[str, COLORS]:
            return ("▇", self.light)

        def get_name(self) -> str:
            return self.name
        
        async def on_start(self) -> None:
            self.horizontal = self.agent.horizontal
            self.name = self.agent.name
            self.environment = self.agent.environment

        async def response(self, message: Message, action: ACTIONS) -> None:
            reply = message.make_reply()
            reply.body = action.value
            await self.send(reply)

        async def change_light(self, await_time: float, action: ACTIONS, color: COLORS) -> None:
            self.light = color
            timeout = await_time / SIMULATION_SPEED
            current_time = time.time()
            msg = None

            while timeout > 0:
                msg = await self.receive(timeout) 
                timeout = (await_time - (time.time() - current_time)) / SIMULATION_SPEED
                if msg:
                    await self.response(msg, action)

            if (not msg or action == ACTIONS.PASS): return
            await self.response(msg, ACTIONS.PASS)


        async def run(self) -> None:
            await self.change_light(5, ACTIONS.STOP, COLORS.RED)
            await self.change_light(5, ACTIONS.PASS, COLORS.GREEN)
            await self.change_light(1, ACTIONS.PASS, COLORS.YELLOW)

    async def setup(self) -> None:
        self.my_behav = self.behav()
        self.add_behaviour(self.my_behav)
