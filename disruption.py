from typing import List
from config import DAY_DURATION
from enums import ACTIONS
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

class DisruptionAgent(Agent):
    def __init__(self, jid: str, password: str) -> None:
        super().__init__(jid, password)

    class behav(CyclicBehaviour):
        async def on_start(self) -> None:
            self.daily_schedule: List[int] = [0 for _ in range(24)]
            self.hour_counter: int = 0

        async def run(self) -> None:

            timer: float = DAY_DURATION
            msg: Message = await self.recieve(timer)
            if not msg: 
                self.hour_counter += 1
                if self.hour_counter == 24:
                    self.hour_counter = 0
                return

            value, addon = msg.body.split(";")
            action = ACTIONS(value)

            if action == ACTIONS.USED:
                self.daily_schedule[self.hour_counter] += 1


    async def setup(self) -> None:
        self.my_behav = self.behav()
        self.add_behaviour(self.my_behav)
