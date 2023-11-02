import time
from environment import Environment
import spade
import curses
import threading

from config import DIRECTIONS

# from traffic_light import TrafficLightAgent
from car import CarAgent

async def main():
    environment = Environment()
    await environment.create_city()

    car = CarAgent("car@localhost", "car", environment, [2,5], DIRECTIONS.EAST)
    car1 = CarAgent("car1@localhost", "car", environment, [5,2], DIRECTIONS.SOUTH)
    await car.start()
    await car1.start()

    time_thread = threading.Thread(target=environment.print_city)
    time_thread.start()

if __name__ == "__main__":
    try:
        spade.run(main())
        curses.endwin()
    except KeyboardInterrupt:
        curses.endwin()
        print("finish")



