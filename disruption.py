from typing import List, Optional
from config import DAY_DURATION
from enums import ACTIONS
from sklearn.linear_model import LinearRegression
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from config import console 

class DisruptionAgent(Agent):
    def __init__(self, jid: str, password: str) -> None:
        super().__init__(jid, password)

    class behav(CyclicBehaviour):
        async def on_start(self) -> None:
            self.daily_schedule: List[int] = [0 for _ in range(24)]
            self.hour_counter: int = 0
            self.modal = LinearRegression()

        async def run(self) -> None:

            timer: float = DAY_DURATION
            msg: Optional[Message] = await self.receive(timer / 5) 
            if not msg: 
                self.hour_counter += 1
                console.addstr(f"{self.hour_counter:02}:00\n")
                if self.hour_counter == 24:
                    hours_of_day = [i for i in range(24)]
                    self.modal.fit(hours_of_day, [i for i in self.daily_schedule])
                    predictions = self.modal.predict(hours_of_day)
                    console.addstr(f"{[hour for hour, pred in zip(hours_of_day, predictions) if pred == min(predictions)]}\n")
                    self.hour_counter = 0
                    self.daily_schedule.clear()
                    self.daily_schedule = [0 for _ in range(24)]
                return

            value, addon = msg.body.split(";")
            action = ACTIONS(value)

            if action == ACTIONS.USED:
                self.daily_schedule[self.hour_counter] += 1


    async def setup(self) -> None:
        self.my_behav = self.behav()
        self.add_behaviour(self.my_behav)
