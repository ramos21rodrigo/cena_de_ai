from disruption import DisruptionAgent
from environment import Environment
import spade
import threading

from enums import COLORS, DIRECTIONS
from config import console, curses, disruption_agent

from car import CarAgent

async def main():
    environment = Environment()
    await environment.create_city()

    disruption = DisruptionAgent(disruption_agent[0], disruption_agent[1], environment)
    await disruption.start()

    console.addstr("Adding cars...\n")
    console.addstr("Console logs:\n\n")
    console.refresh()
    car = CarAgent("car@localhost", "car", environment, [5,2], DIRECTIONS.EAST, COLORS.WHITE, 1)
    car1 = CarAgent("car1@localhost", "car", environment, [4,2], DIRECTIONS.SOUTH, COLORS.WHITE, 1)
    emergency = CarAgent("car2@localhost", "car", environment, [5,2], DIRECTIONS.SOUTH, COLORS.BLUE, 10)
    #car2 = CarAgent("car2@localhost", "car", environment, [3,2], DIRECTIONS.SOUTH)
    #car = CarAgent("car@localhost", "car", environment, [1,38], DIRECTIONS.EAST)
    #car1 = CarAgent("car1@localhost", "car", environment, [1,41], DIRECTIONS.EAST)
    await car.start()
    await car1.start()
    await emergency.start()
    #await car2.start()

    time_thread = threading.Thread(target=environment.print_city)
    time_thread.daemon = True
    time_thread.start()

if __name__ == "__main__":
    try:
        spade.run(main())
    except KeyboardInterrupt:
        curses.endwin()
        print("finish")

