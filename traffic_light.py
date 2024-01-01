import math
import time
from typing import List, Optional, Tuple
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from config import TRAFFIC_LIGHT_WAIT_TIME, URGENCY_GAP, disruption_agent, console
from enums import ACTIONS, COLORS, DIRECTIONS, PERFORMATIVES, TYPE

class TrafficLightAgent(Agent):
    def __init__(self, jid: str, password: str, environment, position: Tuple[int, int]) -> None:
        super().__init__(jid, password)
        self.position = position
        self.environment = environment

    class behav(CyclicBehaviour):
        def get_character(self) -> Tuple[str, COLORS]:
            if self.go_to in [DIRECTIONS.NORTH, DIRECTIONS.SOUTH]:
                return ("-", self.light)
            return ("|", self.light)
        
        def get_name(self) -> str:
            return self.name

        # get neighbors traffic light
        def configure_traffic_light(self) -> None:
            cos: int = round(math.cos(math.radians(self.go_to.value)))
            sin: int = round(math.sin(math.radians(self.go_to.value)))
            for i in range(1, 4):
                for j in range(-2, 2):
                    space: Optional[str] = self.environment.get_agent_in_position((
                        self.position[0] - (i * sin) + (j * cos),
                        self.position[1] + (i * cos) + (j * sin),
                    ))
                    if space: self.neighbor_traffic_names.append(f"{space}@localhost")
        
        async def on_start(self) -> None:
            # environment: Environment avoid circular dependency

            self.position: Tuple[int, int] = self.agent.position
            self.name: str = self.agent.name
            self.environment = self.agent.environment

            self.neighbor_traffic_names: List[str] = []
            self.go_to: DIRECTIONS = DIRECTIONS.NONE
            self.light: COLORS = COLORS.RED

            self.green_light_starter_timer: float = TRAFFIC_LIGHT_WAIT_TIME
            self.green_light_timer: float = 0
            self.await_timeout: float = 99999999
            self.urgency_level: int = 0
            self.order: int = 1

            self.change_color_accepted: int = 0
            self.stopped_car: Optional[str] = None

            for i in range(0, 360, 90): 
                if self.environment.get_schema_in_position((
                        self.position[0] - round(math.sin(math.radians(i))),
                        self.position[1] + round(math.cos(math.radians(i))))) == TYPE.WALL:
                            self.go_to = DIRECTIONS((i + 90) % 360)
                            break


        async def send_message(self, to: Optional[str], performative: PERFORMATIVES, body: Optional[ACTIONS] = None, addons: str = "") -> None:
            if not to: return

            msg: Message = Message(to)
            msg.set_metadata("performative", performative.value)
            if body: msg.body = f"{body.value};{addons}"
                        
            await self.send(msg)
 
        async def run(self) -> None:

            timer: float = time.time()
            msg: Optional[Message] = await self.receive(self.await_timeout) 

            if not msg:
                self.await_timeout = 999999
                self.light = COLORS.YELLOW
                for traffic in self.neighbor_traffic_names:
                    await self.send_message(traffic, PERFORMATIVES.REQUEST, ACTIONS.CHANGE_COLOR, str(self.urgency_level))
                return

            if self.await_timeout <= self.green_light_starter_timer:
                self.await_timeout -= time.time() - timer # 20s - now(1000) - before self.recieve(995) = 15s
                if self.await_timeout < 0: self.await_timeout = 0

            value, addon = msg.body.split(";")
            action = ACTIONS(value)

            if action == ACTIONS.GREEN_LIGHT_TIMER:
                self.green_light_starter_timer = float(addon)

            if action == ACTIONS.OFF:
                console.addstr(f"{self.name} lights: OFF\n")
                self.await_timeout = 999999
                self.light = COLORS.GRAY
                if self.stopped_car:
                    await self.send_message(self.stopped_car, PERFORMATIVES.INFORM, ACTIONS.PASS)

            if action == ACTIONS.ON and self.light == COLORS.GRAY:
                console.addstr(f"{self.name} lights: ON\n")
                self.light = COLORS.RED

            if action == ACTIONS.ASK_FOR_ACTION:
                await self.send_message(disruption_agent[0], PERFORMATIVES.INFORM, ACTIONS.USED)
                if self.light in [COLORS.GREEN, COLORS.GRAY]:
                    await self.send_message(str(msg.sender), PERFORMATIVES.INFORM, ACTIONS.PASS)
                    return

                self.urgency_level += int(addon)
                self.light = COLORS.YELLOW
                self.stopped_car = str(msg.sender)
                await self.send_message(self.stopped_car, PERFORMATIVES.INFORM, ACTIONS.STOP)
                for traffic in self.neighbor_traffic_names:
                    await self.send_message(traffic, PERFORMATIVES.REQUEST, ACTIONS.CHANGE_COLOR, str(self.urgency_level))
                return

            if action == ACTIONS.CHANGE_COLOR:
                self.green_light_timer -= time.time() - timer
                if self.green_light_timer <= 0 or self.urgency_level + URGENCY_GAP < int(addon): ## Allowded
                    self.urgency_level = 0
                    self.light = COLORS.RED
                    self.green_light_timer = 0
                    self.order = 1
                    await self.send_message(str(msg.sender), PERFORMATIVES.INFORM, ACTIONS.ALLOW)
                    return
                await self.send_message(str(msg.sender), PERFORMATIVES.INFORM, ACTIONS.DENY, str(self.green_light_timer + self.order))
                self.order += 1
                return

            if action == ACTIONS.ALLOW:
                self.change_color_accepted += 1
                if self.change_color_accepted >= len(self.neighbor_traffic_names):
                    self.change_color_accepted = 0
                    self.urgency_level = 1
                    self.light = COLORS.GREEN
                    await self.send_message(self.stopped_car, PERFORMATIVES.INFORM, ACTIONS.PASS)
                    if self.green_light_timer <= 0:
                        self.green_light_timer = self.green_light_starter_timer
                return

            if action == ACTIONS.DENY:
                self.await_timeout = float(addon) #20s
                self.change_color_accepted -= len(self.neighbor_traffic_names) - 1 # if accepted == 2 it still needs 1+ for 0

    async def setup(self) -> None:
        self.my_behav = self.behav()
        self.add_behaviour(self.my_behav)
