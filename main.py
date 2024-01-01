from environment import Environment
import spade
import threading

from config import DIRECTIONS, curses

from car import CarAgent

async def main():
    environment = Environment()
    await environment.generate()

    #disruption = DisruptionAgent(disruption_agent[0], disruption_agent[1], environment)
    #await disruption.start()

    car = CarAgent("car@localhost", "car", environment, [5,2], DIRECTIONS.EAST, False)
    car1 = CarAgent("car1@localhost", "car", environment, [4,2], DIRECTIONS.SOUTH, False)
    emergency = CarAgent("car2@localhost", "car", environment, [5,2], DIRECTIONS.SOUTH, True)
    await car.start()
    await car1.start()
    await emergency.start()

    time_thread = threading.Thread(target=environment.print_city)
    time_thread.daemon = True
    time_thread.start()

if __name__ == "__main__":
    try:
        spade.run(main())
    except KeyboardInterrupt:
        curses.endwin()
        print("finish")

