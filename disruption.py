import time 
from typing import Dict, List, Optional, Tuple
import numpy as np
from config import DAY_DURATION, SIMULATION_SPEED, TRAFFIC_LIGHT_WAIT_TIME
from enums import ACTIONS, PERFORMATIVES
from sklearn.linear_model import LinearRegression
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from config import console, clock
from environment import Environment

class DisruptionAgent(Agent):
    def __init__(self, jid: str, password: str, environment: Environment) -> None:
        super().__init__(jid, password)
        self.environment = environment

    class behav(CyclicBehaviour):
        async def on_start(self) -> None:
            self.model: LinearRegression = LinearRegression()
            self.model_green: LinearRegression = LinearRegression()

            self.used_traffics: List[str] = self.agent.environment.get_used_traffics()
            self.traffics: Dict[str, int] = {i: 0 for i in self.used_traffics}

            self.daily_schedule: List[int] = [0 for _ in range(24)]
            self.hour_counter: int = 0
            self.time_left: float = DAY_DURATION
            self.lowest_hours: List[int] = []

            clock.addstr("24:00 -> 0x")


        async def send_message(self, to: Optional[str], performative: PERFORMATIVES, body: Optional[ACTIONS] = None, addons: str = "") -> None:
            if not to: return

            msg: Message = Message(to)
            msg.set_metadata("performative", performative.value)
            if body: msg.body = f"{body.value};{addons}"
                        
            await self.send(msg)

        async def run(self) -> None:

            timer: float = time.time()
            msg: Optional[Message] = await self.receive(self.time_left) 
            if not msg: 
                self.hour_counter += 1
                clock.clear()
                clock.addstr(f"{self.hour_counter:02}:00 -> {self.daily_schedule[self.hour_counter - 1]}x")
                self.time_left = DAY_DURATION

                if self.hour_counter == 24:
                    hours_of_day = [i for i in range(24)]
                    X = np.array(hours_of_day).reshape(-1, 1)

                    self.model.fit(X, self.daily_schedule)
                    predictions = self.model.predict(X)

                    min_prediction = min(predictions)
                    self.lowest_hours = [hour for hour, pred in zip(hours_of_day, predictions) if pred == min_prediction]

                    for light, usage_count in self.traffics.items():
                        self.model_green.fit([[usage_count]], [usage_count])
                    
                        green_light_duration = TRAFFIC_LIGHT_WAIT_TIME + int(self.model_green.predict([[usage_count]])[0]) / SIMULATION_SPEED
                        console.addstr(f"{light.split('@')[0]}: {green_light_duration}s\n")
                        await self.send_message(light, PERFORMATIVES.INFORM, ACTIONS.GREEN_LIGHT_TIMER, str(green_light_duration))

                    self.hour_counter = 0
                    self.daily_schedule = [0 for _ in range(24)]
                    self.traffics = {i: 0 for i in self.used_traffics}
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
                self.traffics[str(msg.sender)] += 1


    async def setup(self) -> None:
        self.my_behav = self.behav()
        self.add_behaviour(self.my_behav)
