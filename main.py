import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from spade import wait_until_finished

from config import DIRECTIONS

# from traffic_light import TrafficLightAgent
from car import CarAgent
from traffic_light import TrafficLightAgent

async def main():
    car = CarAgent("car@localhost", "car", [1, 2], DIRECTIONS.EAST)
    light = TrafficLightAgent("traffic@localhost", "traffic")
    await car.start()
    await light.start()

    await wait_until_finished(car)


if __name__ == "__main__":
    spade.run(main())

