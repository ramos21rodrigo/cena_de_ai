import asyncio
import random
import math
from typing import List, Optional, Tuple
from environment import TYPE
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from config import SIMULATION_SPEED
from enums import ACTIONS, COLORS, DIRECTIONS, PERFORMATIVES

class CarAgent(Agent):

    def __init__(self, jid, password, environment, position, direction, color, urgency_level):
        super().__init__(jid, password)
        self.position = position
        self.direction = direction
        self.environment = environment
        self.color = color
        self.urgency_level = urgency_level

    class behav(CyclicBehaviour):
        # environment: Environment avoid circular dependency
        arrows: dict[DIRECTIONS, str] = {
            DIRECTIONS.NORTH: "↑",
            DIRECTIONS.SOUTH: "↓",
            DIRECTIONS.EAST: "→",
            DIRECTIONS.WEST:"←"
        }

        def get_position(self) -> List[int]:
            return self.position

        def get_name(self) -> str:
            return self.name

        def get_arrow(self) -> Tuple[str, COLORS]:
            return (self.arrows.get(self.direction, "*"), self.color)

        async def on_start(self) -> None:
            self.position: List[int] = self.agent.position
            self.name: str = self.agent.name
            self.environment = self.agent.environment
            self.direction: DIRECTIONS = self.agent.direction
            self.color: COLORS = self.agent.color
            self.urgency_level: int = self.agent.urgency_level

        async def send_message(self, to: str, performative: PERFORMATIVES, body: Optional[ACTIONS] = None, addons: str = "") -> None:
            if not to: return

            msg: Message = Message(to)
            msg.set_metadata("performative", performative.value)
            
            if body: msg.body = f"{body.value};{addons}"
                        
            await self.send(msg)

        async def handle_communication(self, to: str) -> bool:
            if not to: return True

            stopped_car: Optional[str] = None
            timeout = 3 / SIMULATION_SPEED
            await self.send_message(f"{to}@localhost", PERFORMATIVES.REQUEST, ACTIONS.ASK_FOR_ACTION, str(self.urgency_level))

            while True:
                response: Optional[Message] = await self.receive(timeout) 
                if not response: return False

                value, addon = response.body.split(";")
                action = ACTIONS(value)

                if action == ACTIONS.STOP:
                    timeout = 99999

                if action == ACTIONS.ASK_FOR_ACTION:
                    stopped_car = str(response.sender)
                    await self.send_message(stopped_car, PERFORMATIVES.INFORM, ACTIONS.STOP)
                    await self.send_message(f"{to}@localhost", PERFORMATIVES.INFORM, ACTIONS.ASK_FOR_ACTION, addon)

                if (action == ACTIONS.PASS): break

            if stopped_car:
                await self.send_message(stopped_car, PERFORMATIVES.INFORM, ACTIONS.PASS)
            return True


        def check_pattern(self, position: List[int], angle: int, line_to_check: int = 1, left_to_right: bool = False) -> bool:
            # find pattern [ROAD, ROAD]
            #                 [line_to_check] (distance between pattern and CAR)
            #                     CAR
            #
            # from the angle [left, right, up] 
            # using the math.sin() and math.cos() functions
    
            angle_radians: float = math.radians(angle)
    
            delta_row: int = -round(math.sin(angle_radians))
            delta_col: int = round(math.cos(angle_radians))
    
            new_row: int = position[0] + delta_row * line_to_check
            new_col: int = position[1] + delta_col * line_to_check
    
            if left_to_right:
                delta_col *= -1
                delta_row *= -1
    
            if new_col < 0 or new_row < 0 or new_row >= self.environment.get_city_height() or new_col >= self.environment.get_city_width():
                return False
    
            second_space: TYPE = self.environment.get_schema_in_position((new_row, new_col))
            third_space: TYPE = self.environment.get_schema_in_position((new_row - delta_col, new_col + delta_row))

            return second_space != TYPE.WALL and third_space != TYPE.WALL

        def try_to_change_direction(self) -> None:
            direction: DIRECTIONS = self.direction
            position: List[int] = self.position

            to_left: int = (direction.value + 90) % 360
            to_right: int = (direction.value - 90) % 360
            directions: List[DIRECTIONS] = []

            if (self.check_pattern(position, direction.value, 2) or self.check_pattern(position, to_left, 2, True)):
                directions.append(direction)
            if (self.check_pattern(position, to_left, 2)):
                directions.append(DIRECTIONS(to_left))
            if (self.check_pattern(position, to_right)):
                directions.append(DIRECTIONS(to_right))

            if len(directions) == 0:
                self.kill()
                return

            if len(directions) >= 1:
                self.direction = random.choice(directions)

        async def move_or_wait(self) -> None:
            new_position = self.position
            new_position[0] -= round(math.sin(math.radians(self.direction.value)))
            new_position[1] += round(math.cos(math.radians(self.direction.value)))
            if await self.handle_communication(self.environment.get_agent_in_position(new_position)):
                self.position = new_position

        async def run(self) -> None:
            self.try_to_change_direction()
            await self.move_or_wait()
            self.environment.update_city(self)
            await asyncio.sleep(1 / SIMULATION_SPEED)
                

    async def setup(self) -> None:
        self.my_behav = self.behav()
        self.add_behaviour(self.my_behav)
