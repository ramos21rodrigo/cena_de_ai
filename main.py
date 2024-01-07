from disruption import DisruptionAgent
from environment import Environment
import spade
import threading

from header import DIRECTIONS, curses

from car import CarAgent

async def main():
    environment = Environment()
    await environment.generate()

    disruption = DisruptionAgent("disruption@localhost",  "disruption")
    await disruption.start()

    car = CarAgent("car@localhost", "car", environment, [5,2], DIRECTIONS.EAST, False)
    car2 = CarAgent("car2@localhost", "car", environment, [5,2], DIRECTIONS.SOUTH, True)
    car1 = CarAgent("car1@localhost", "car", environment, [4,2], DIRECTIONS.SOUTH, False)
    await car.start()
    await car1.start()
    await car2.start()

    time_thread = threading.Thread(target=environment.print_city)
    time_thread.daemon = True
    time_thread.start()

if __name__ == "__main__":
    try:
        spade.run(main())
    except KeyboardInterrupt:
        curses.endwin()
        print("finish")

