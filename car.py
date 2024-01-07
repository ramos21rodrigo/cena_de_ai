import asyncio
import random
import math
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from header import ACTIONS, DIRECTIONS, TYPE

class CarAgent(Agent):

    def __init__(self, jid, password, environment, position, direction, urgent):
        super().__init__(jid, password)
        self.environment = environment
        self.position = position
        self.direction = direction
        self.urgent = urgent

    class behav(CyclicBehaviour):
        async def on_start(self):
            self.position = self.agent.position
            self.name = self.agent.name
            self.environment = self.agent.environment
            self.direction = self.agent.direction
            self.urgent = self.agent.urgent
            self.speed = 0.25
            await self.send_message("disruption@localhost", "inform", ACTIONS.CONNECT)

        async def send_message(self, to, performative, body = None, addons: str = ""):
            msg = Message(to)
            msg.set_metadata("performative", performative)
            if body: msg.body = f"{body.value};{addons}"
            await self.send(msg)

        async def handle_communication(self, to):
            if not to: return True

            timeout = 3
            stopped_car = ""
            await self.send_message(f"{to}@localhost", "request", ACTIONS.ASK_FOR_ACTION, str(self.urgent))

            while True:
                msg = await self.receive(timeout) 
                if not msg: return False

                value, additional_info = msg.body.split(";")
                sender = str(msg.sender)
                action = ACTIONS(value)

                if (action == ACTIONS.PASS): 
                    if stopped_car:
                        await self.send_message(stopped_car, "inform", ACTIONS.PASS)
                    return True

                #if action == ACTIONS.UPDATE_SPEED:
                    self.speed = 0.25 + (0.25 * int(additional_info)) 

                if action == ACTIONS.STOP:
                    timeout = 1000000

                if action == ACTIONS.ASK_FOR_ACTION:
                    stopped_car = sender
                    await self.send_message(stopped_car, "inform", ACTIONS.STOP)
                    await self.send_message(f"{to}@localhost", "inform", ACTIONS.ASK_FOR_ACTION, additional_info)


        def check_pattern(self, position, angle, line_to_check = 1, left_to_right = False):
            angle_radians = math.radians(angle)
    
            delta_row = -round(math.sin(angle_radians))
            delta_col = round(math.cos(angle_radians))
    
            new_row = position[0] + delta_row * line_to_check
            new_col = position[1] + delta_col * line_to_check
    
            if left_to_right:
                delta_col *= -1
                delta_row *= -1
    
            if new_col < 0 or new_row < 0 or new_row >= self.environment.city_height or new_col >= self.environment.city_width:
                return False
    
            second_space = self.environment.city_schema[new_row][new_col]
            third_space = self.environment.city_schema[new_row - delta_col][new_col + delta_row]

            return second_space != TYPE.WALL and third_space != TYPE.WALL

        def try_to_change_direction(self):
            direction = self.direction
            position = self.position

            to_left = (direction.value + 90) % 360
            to_right = (direction.value - 90) % 360
            directions = []

            if (self.check_pattern(position, direction.value, 2) or self.check_pattern(position, to_left, 2, True)):
                directions.append(direction)
            if (self.check_pattern(position, to_left, 2)):
                directions.append(DIRECTIONS(to_left))
            if (self.check_pattern(position, to_right)):
                directions.append(DIRECTIONS(to_right))

            if len(directions) == 0:
                self.kill()
            elif len(directions) >= 1:
                self.direction = random.choice(directions)

        async def move_or_wait(self):
            new_position = self.position
            new_position[0] -= round(math.sin(math.radians(self.direction.value)))
            new_position[1] += round(math.cos(math.radians(self.direction.value)))
            if await self.handle_communication(self.environment.get_agent(new_position)):
                self.position = new_position

        async def run(self):
            self.try_to_change_direction()
            await self.move_or_wait()
            self.environment.update_city(self)
            await asyncio.sleep(self.speed)
                

    async def setup(self):
        self.my_behav = self.behav()
        self.add_behaviour(self.my_behav)
