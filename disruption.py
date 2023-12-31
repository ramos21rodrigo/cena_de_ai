import time 
from typing import List, Optional
import numpy as np
from config import DAY_DURATION
from enums import ACTIONS, PERFORMATIVES
from sklearn.linear_model import LinearRegression
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from config import console
from environment import Environment

class DisruptionAgent(Agent):
    def __init__(self, jid: str, password: str, environment: Environment) -> None:
        super().__init__(jid, password)
        self.environment = environment

    class behav(CyclicBehaviour):
        async def on_start(self) -> None:
            self.used_traffics: List[str] = self.agent.environment.get_used_traffics()
            self.daily_schedule: List[int] = [0 for _ in range(24)]
            self.hour_counter: int = 0
            self.modal = LinearRegression()
            self.time_left: float = DAY_DURATION
            self.lowest_hours: List[int] = []

        async def send_message(self, to: Optional[str], performative: PERFORMATIVES, body: Optional[ACTIONS] = None) -> None:
            if not to: return

            msg: Message = Message(to)
            msg.set_metadata("performative", performative.value)
            if body: msg.body = f"{body.value};"
                        
            await self.send(msg)

        async def run(self) -> None:

            timer: float = time.time()
            msg: Optional[Message] = await self.receive(self.time_left / 5) 
            if not msg: 
                self.hour_counter += 1
                console.addstr(f"{self.hour_counter:02}:00 -> {self.daily_schedule[self.hour_counter - 1]} calls\n")
                self.time_left = DAY_DURATION

                if self.hour_counter == 24:
                    hours_of_day = [i for i in range(24)]
                    X = np.array(hours_of_day).reshape(-1, 1)

                    self.modal.fit(X, self.daily_schedule)
                    predictions = self.modal.predict(X)

                    min_prediction = min(predictions)
                    self.lowest_hours = [hour for hour, pred in zip(hours_of_day, predictions) if pred == min_prediction]
				
                    self.hour_counter = 0
                    self.daily_schedule = [0 for _ in range(24)]
                    return
            
                action = ACTIONS.OFF if self.hour_counter in self.lowest_hours else ACTIONS.ON
                for traffic in self.used_traffics:
                    await self.send_message(traffic, PERFORMATIVES.INFORM, action)
                return

            self.time_left -= time.time() - timer
            value, addon = msg.body.split(";")
            action = ACTIONS(value)

            if action == ACTIONS.USED:
                self.daily_schedule[self.hour_counter] += 1


    async def setup(self) -> None:
        self.my_behav = self.behav()
        self.add_behaviour(self.my_behav)
