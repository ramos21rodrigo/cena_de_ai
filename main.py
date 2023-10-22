from environment import Environment
import spade

from spade import wait_until_finished

from config import DIRECTIONS

# from traffic_light import TrafficLightAgent
from car import CarAgent
from traffic_light import TrafficLightAgent

async def main():

    environment = Environment()

    car = CarAgent("car@localhost", "car", environment, [2,4], DIRECTIONS.EAST)
    car1 = CarAgent("car1@localhost", "car", environment, [7,3], DIRECTIONS.NORTH)
    #light = TrafficLightAgent("traffic@localhost", "traffic", environment)
    await car.start()
    await car1.start()

    #await wait_until_finished(car)


if __name__ == "__main__":
    spade.run(main())

