import asyncio
from environment import Environment
import spade
import curses

from config import DIRECTIONS

# from traffic_light import TrafficLightAgent
from car import CarAgent


async def main():

    environment = Environment()

    car = CarAgent("car@localhost", "car", environment, [2,4], DIRECTIONS.EAST)
    car1 = CarAgent("car1@localhost", "car", environment, [7,3], DIRECTIONS.NORTH)
    #light = TrafficLightAgent("traffic@localhost", "traffic", environment)
    await car.start()
    await car1.start()

    #await wait_until_finished(car)

if __name__ == "__main__":
    try:
        spade.run(main())
    except KeyboardInterrupt:
        curses.endwin()
        print("finish")

