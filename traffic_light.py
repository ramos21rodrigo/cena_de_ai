from typing import List, Optional, Tuple
import time
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from config import SIMULATION_SPEED
from enums import ACTIONS, COLORS

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
            if (self.horizontal):
                return ("-", self.light)
            return ("|", self.light)

        def get_name(self) -> str:
            return self.name
        
        async def on_start(self) -> None:
            self.horizontal = self.agent.horizontal
            self.name = self.agent.name
            self.environment = self.agent.environment

        async def send_message(self, to: str, metadata: List[Tuple[str, str]], body: Optional[str] = None) -> None:
            msg: Message = Message(to)
            for data in metadata:
                msg.set_metadata(data[0], data[1])
            if body: msg.body = body
                        
            await self.send(msg)

        async def change_light(self, await_time: float, action: ACTIONS, color: COLORS) -> None:
            self.light = color
            timeout: float = await_time / SIMULATION_SPEED
            current_time: float = time.time()
            msg: Message = None
            stopped_car: Message = None

            while timeout > 0:
                msg = await self.receive(timeout) 
                timeout = (await_time - (time.time() - current_time)) / SIMULATION_SPEED
                if msg:
                    await self.send_message(str(msg.sender), [("performative", "inform")], action.value)
                    stopped_car = str(msg.sender)

            if (not stopped_car or action == ACTIONS.PASS): return
            await self.send_message(stopped_car, [("performative", "inform")], ACTIONS.PASS.value)


        async def run(self) -> None:
            await self.change_light(5, ACTIONS.STOP, COLORS.RED)
            await self.change_light(5, ACTIONS.PASS, COLORS.GREEN)
            await self.change_light(1, ACTIONS.PASS, COLORS.YELLOW)

    async def setup(self) -> None:
        self.my_behav = self.behav()
        self.add_behaviour(self.my_behav)
