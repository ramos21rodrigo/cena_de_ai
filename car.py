import asyncio
import random
import math
from typing import List
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from config import ACTIONS, SIMULATION_SPEED, DIRECTIONS

class CarAgent(Agent):

    def __init__(self, jid, password, environment, position, direction):
        super().__init__(jid, password)
        self.position = position
        self.direction = direction
        self.environment = environment

    class behav(CyclicBehaviour):
        position: List[int]
        direction: DIRECTIONS
        name: str
        # environment: Environment avoid circular dependency
        stop: bool = False

        def get_position(self):
            return self.position

        def get_name(self):
            return self.name

        def get_arrow(self):
            if(self.direction == DIRECTIONS.NORTH):
                return "↑"
            if(self.direction == DIRECTIONS.SOUTH):
                return "↓"
            if(self.direction == DIRECTIONS.EAST):
                return "→"
            return "←" # self.direction == DIRECTIONS.WEST

        async def on_start(self):
            self.position = self.agent.position
            self.name = self.agent.name
            self.environment = self.agent.environment
            self.direction = self.agent.direction

        async def ask_for_instruction(self, to: str) -> ACTIONS:
            msg = Message("{}@localhost".format(to))
            msg.set_metadata("performative", "request")
            msg.set_metadata("request", "light color")
            await self.send(msg)

            response = await self.receive(999)
            if not response: exit()
            return ACTIONS(response.body) 

        async def move_or_wait(self):
            new_position = self.position
            new_position[0] -= round(math.sin(math.radians(self.direction.value)))
            new_position[1] += round(math.cos(math.radians(self.direction.value)))

            to = self.environment.get_position(position=new_position)
            while to:
                instruction: ACTIONS = await self.ask_for_instruction(to)
                if (instruction == ACTIONS.PASS): break

                await asyncio.sleep(1 / SIMULATION_SPEED)
            self.position = new_position

        async def run(self):

            directions = self.environment.get_possible_directions(position=self.position, direction=self.direction)

            if len(directions) == 0:
                self.kill()
                return

            if len(directions) >= 1:
                self.direction = random.choice(directions)

            await self.move_or_wait()
            self.environment.update_city(self)
            await asyncio.sleep(1 / SIMULATION_SPEED)
                

    async def setup(self):
        self.my_behav = self.behav()
        self.add_behaviour(self.my_behav)
