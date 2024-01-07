from asyncio import sleep
import random
from header import ACTIONS, logs
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

def generate_random_accidents():
    return [random.randint(1, 80) for _ in range(30)]

class DisruptionAgent(Agent):
    def __init__(self, jid, password): 
        super().__init__(jid, password)

    class behav(CyclicBehaviour):
        async def on_start(self):
            self.weathers = ["sunny","rainy", "snowy", "clear", "foggy"]
            self.cars = []

            weather_conditions = {weather: generate_random_accidents() for weather in self.weathers}
            X = []
            y = []
            
            for weather, accidents in weather_conditions.items():
                X.extend([weather] * len(accidents))
                y.extend(accidents)

            unique_weather_conditions = list(set(X))
            self.weather_mapping = {weather: index for index, weather in enumerate(unique_weather_conditions)}
            X_encoded = [self.weather_mapping[weather] for weather in X]

            self.model = LinearRegression()
            self.model.fit([[x] for x in X_encoded], y)

        async def send_message(self, to, performative, body = None, addons = ""):
            msg = Message(to)
            msg.set_metadata("performative", performative)
            if body: msg.body = f"{body.value};{addons}"
            await self.send(msg)

        def predict_accidents_for_weather(self, weather_condition):
            if weather_condition in self.weather_mapping:
                encoded_weather = self.weather_mapping[weather_condition]
                predicted_accidents = self.model.predict([[encoded_weather]])
                return predicted_accidents[0]
            return 0

        async def run(self):
            msg = await self.receive(5)
            if not msg: 
                chosen_weather = random.choice(self.weathers)

                predicted_values = int(self.predict_accidents_for_weather(chosen_weather))
                logs.addstr(f"{chosen_weather}: speed -{predicted_values}%\n")
                for car in self.cars:
                    await self.send_message(car, "request", ACTIONS.UPDATE_SPEED, str(predicted_values))
                return

            value, additional_info = msg.body.split(";")
            sender = str(msg.sender)
            action = ACTIONS(value)

            if action == action.CONNECT:
                self.cars.append(sender)

    async def setup(self) -> None:
        self.my_behav = self.behav()
        self.add_behaviour(self.my_behav)
