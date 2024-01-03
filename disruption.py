from asyncio import sleep
import time 
import numpy as np
import random
from header import ACTIONS, TRAFFIC_LIGHT_WAIT_TIME, console
from sklearn.linear_model import LinearRegression
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from environment import Environment






def generate_random_accidents():
    return [random.randint(1, 80) for _ in range(30)]

class DisruptionAgent(Agent):
    def __init__(self, jid, password): 
        super().__init__(jid, password)

    class behav(CyclicBehaviour):
        async def on_start(self):
            weather_conditions = {
                "sunny": generate_random_accidents(),
                "rainy": generate_random_accidents(),
                "snowy": generate_random_accidents(),
                "clear": generate_random_accidents(),
                "foggy": generate_random_accidents(),
            }
            data = []
            targets = []

            for weather, accidents in weather_conditions.items():
                for accident in accidents:
                    data.append([accident, weather])
                    targets.append(weather)

            self.model = LinearRegression()
            self.model.fit(data, targets)

        async def send_message(self, to, performative, body = None, addons = ""):
            msg = Message(to)
            msg.set_metadata("performative", performative)
            if body: msg.body = f"{body.value};{addons}"
            await self.send(msg)
            def predict_accidents_for_weather(self, weather_condition):
                accidents = generate_random_accidents()
                predicted_accidents = self.model.predict([[accident, weather_condition] for accident in accidents])
                return predicted_accidents

        async def run(self):

            await sleep(20)
            chosen_weather = "sunny" 

            predicted_values = self.predict_accidents_for_weather(chosen_weather)
            console.addstr(f"Predicted accident values for {chosen_weather} weather: {predicted_values}")



    async def setup(self) -> None:
        self.my_behav = self.behav()
        self.add_behaviour(self.my_behav)
