import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from enum import Enum

class Colors(Enum):
    GREEN = "green",
    YELLOW = "yellow",
    RED = "red"

class TrafficLightAgent(Agent):
    class behave(CyclicBehaviour):
        
        counter: int = 0

        async def on_start(self):
            print("Starting behaviour . . .")

        async def run(self):
            print("Counter: {}".format(self.counter))
            print(Colors.RED)
            self.counter += 1
            await asyncio.sleep(1)

        async def on_end(self):
            print("Behaviour finished with exit code {}.".format(self.exit_code))

    async def setup(self):
        print("Agent starting . . .")
        self.my_behav = self.behave()
        self.add_behaviour(self.my_behav)
