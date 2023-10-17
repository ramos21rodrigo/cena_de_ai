import asyncio
from typing import List
from environment import TYPE
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from config import SIMULATION_SPEED, DIRECTIONS

from enum import Enum

class COLORS(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"

class TrafficLightAgent(Agent):
    class behave(CyclicBehaviour):
        position: List[int]
        ligth: COLORS

        def get_position(self):
            return self.position

        def get_type(self):
            return TYPE.LIGHT

        def get_light(self):
            return self.ligth
        
#        async def on_start(self):

        async def run(self):
            self.light = COLORS.GREEN
            await asyncio.sleep(10 / SIMULATION_SPEED)
            self.light = COLORS.YELLOW
            await asyncio.sleep(1 / SIMULATION_SPEED)
            self.light = COLORS.RED
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
       

