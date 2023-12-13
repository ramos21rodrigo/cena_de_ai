from environment import Environment
import spade
import threading

from enums import DIRECTIONS
from config import city, curses

from car import CarAgent

async def main():
    environment = Environment()
    await environment.create_city()

    city.addstr("\nAdding cars...\n")
    city.refresh()
    car = CarAgent("car@localhost", "car", environment, [5,2], DIRECTIONS.EAST)
    car1 = CarAgent("car1@localhost", "car", environment, [4,2], DIRECTIONS.SOUTH)
    #car = CarAgent("car@localhost", "car", environment, [1,38], DIRECTIONS.EAST)
    #car1 = CarAgent("car1@localhost", "car", environment, [1,41], DIRECTIONS.EAST)
    await car.start()
    await car1.start()

    time_thread = threading.Thread(target=environment.print_city)
    time_thread.daemon = True
    time_thread.start()

if __name__ == "__main__":
    try:
        spade.run(main())
    except KeyboardInterrupt:
        curses.endwin()
        print("finish")

