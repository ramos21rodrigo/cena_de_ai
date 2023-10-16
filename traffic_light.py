import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from config import SIMULATION_SPEED, DIRECTIONS

from enum import Enum, auto

class Colors(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"

class TrafficLightAgent(Agent):
    class behave(CyclicBehaviour):
        
#        async def on_start(self):

        async def run(self):
            print(Colors.GREEN.value)
            await asyncio.sleep(10 / SIMULATION_SPEED)
            print(Colors.YELLOW.value)
            await asyncio.sleep(1 / SIMULATION_SPEED)
            print(Colors.RED.value)
            await asyncio.sleep(10 / SIMULATION_SPEED)

#        async def on_end(self):

    async def setup(self):
        self.my_behav = self.behave()
        self.add_behaviour(self.my_behav)


class Clustter:
    north: TrafficLightAgent
    south: TrafficLightAgent
    east: TrafficLightAgent
    west: TrafficLightAgent

    def __init__(self, north: TrafficLightAgent, south: TrafficLightAgent, east: TrafficLightAgent, west: TrafficLightAgent
                 ) -> None:
        self.north = north
        self.south = south
        self.east = east
        self.west = west

    def get_light(self, direciton): 
        if (direciton == DIRECTIONS.NORTH):
            return self.north
        if (direciton == DIRECTIONS.SOUTH):
            return self.south
        if (direciton == DIRECTIONS.WEST):
            return self.west
        if (direciton == DIRECTIONS.EAST):
            return self.east
       

