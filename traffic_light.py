import math
import time
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from config import TRAFFIC_LIGHT_WAIT_TIME, ACTIONS, COLORS, DIRECTIONS, TYPE

class TrafficLightAgent(Agent):
    def __init__(self, jid, password, environment, position):
        super().__init__(jid, password)
        self.position = position
        self.environment = environment

    class behav(CyclicBehaviour):
        def get_name(self):
            return self.name

        def configure_traffic_light(self) -> None:
            cos = round(math.cos(math.radians(self.go_to.value)))
            sin = round(math.sin(math.radians(self.go_to.value)))
            for i in range(1, 4):
                for j in range(-2, 2):
                    space = self.environment.get_agent((
                        self.position[0] - (i * sin) + (j * cos),
                        self.position[1] + (i * cos) + (j * sin),
                    ))
                    if space: self.neighbor_traffic_names.append(f"{space}@localhost")
        
        async def on_start(self) -> None:
            self.position = self.agent.position
            self.name = self.agent.name
            self.environment = self.agent.environment

            self.neighbor_traffic_names = []
            self.light = COLORS.RED

            self.green_light_timer = 0
            self.call_again = False
            self.change_color_accepted = 0

            for i in range(0, 360, 90): 
                if self.environment.city_schema[self.position[0] - round(math.sin(math.radians(i)))][self.position[1] + round(math.cos(math.radians(i)))] == TYPE.WALL:
                            self.go_to = DIRECTIONS((i + 90) % 360)
                            break


        async def send_message(self, to, performative, body = None, addons: str = ""):
            msg = Message(to)
            msg.set_metadata("performative", performative)
            if body: msg.body = f"{body.value};{addons}"
            await self.send(msg)
 
        async def run(self):

            timer: float = time.time()
            msg = await self.receive(3 if self.call_again else 100000) 
            if not msg:
                self.call_again = False
                self.light = COLORS.YELLOW
                for traffic in self.neighbor_traffic_names:
                    await self.send_message(traffic, "request", ACTIONS.CHANGE_COLOR)
                return

            value, additional_info = msg.body.split(";")
            sender = str(msg.sender)
            action = ACTIONS(value)

            if action == ACTIONS.CHANGE_COLOR:
                self.green_light_timer -= time.time() - timer
                if self.green_light_timer <= 0 or additional_info == "True":
                    self.light = COLORS.RED
                    self.green_light_timer = 0
                    await self.send_message(sender, "inform", ACTIONS.ALLOW)
                else:
                    await self.send_message(msg, "inform", ACTIONS.DENY)

            elif action == ACTIONS.ALLOW:
                self.change_color_accepted += 1
                if self.change_color_accepted >= len(self.neighbor_traffic_names):
                    self.change_color_accepted = 0
                    self.urgency_level = 1
                    self.light = COLORS.GREEN
                    await self.send_message(self.stopped_car, "inform", ACTIONS.PASS)
                    if self.green_light_timer <= 0:
                        self.green_light_timer = TRAFFIC_LIGHT_WAIT_TIME

            elif action == ACTIONS.ASK_FOR_ACTION:
                if self.light == COLORS.GREEN:
                    await self.send_message(sender, "inform", ACTIONS.PASS)
                else:
                    self.light = COLORS.YELLOW
                    self.stopped_car = sender
                    await self.send_message(self.stopped_car, "inform", ACTIONS.STOP)
                    for traffic in self.neighbor_traffic_names:
                        await self.send_message(traffic, "request", ACTIONS.CHANGE_COLOR, additional_info)

            elif action == ACTIONS.DENY:
                self.call_again = True
                self.change_color_accepted -= len(self.neighbor_traffic_names) - 1

    async def setup(self) -> None:
        self.my_behav = self.behav()
        self.add_behaviour(self.my_behav)
