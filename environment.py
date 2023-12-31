import asyncio
import curses
from typing import List, Optional, Tuple,  Union
import time

from config import MAP_FILE, traffic_agents, SIMULATION_SPEED, city, stdscr, console, clock
from enums import COLORS, TYPE

from traffic_light import TrafficLightAgent
from car import CarAgent

class Environment:
    city_schema: List[List[Union[TrafficLightAgent.behav, TYPE]]]
    city: List[List[Optional[CarAgent.behav]]]
    city_height: int
    city_width: int
    used_traffics: List[str]

    def get_used_traffics(self) -> List[str]:
        return self.used_traffics

    def get_city_height(self) -> int:
        return self.city_height

    def get_city_width(self) -> int:
        return self.city_width

    def get_schema_in_position(self, position: Tuple[int, int]) -> Union[TrafficLightAgent.behav, TYPE]:
        return self.city_schema[position[0]][position[1]]

    def get_agent_in_position(self, position: Tuple[int, int]) -> Optional[str]:
        if isinstance(self.city[position[0]][position[1]], CarAgent.behav):
            return self.city[position[0]][position[1]].get_name()
        if isinstance(self.city_schema[position[0]][position[1]], TrafficLightAgent.behav): 
            return self.city_schema[position[0]][position[1]].get_name()
        return None

    async def create_city(self) -> None:
        agents: List[TrafficLightAgent.behav] = []
        file = open(MAP_FILE, "r")
        content = file.readlines()

        console.addstr("Creating city...\n")
        console.refresh()
        self.used_traffics = []
        self.city_height = len(content)
        self.city_width = len(content[0]) - 1
        self.city_schema = [[TYPE.ROAD for i in range(self.city_width)] for j in range(self.city_height)]
        self.city = [[None for i in range(self.city_width)] for j in range(self.city_height)]
        
        for i in range(self.city_height):
            for j in range(self.city_width):
                if (content[i][j] == TYPE.LIGHT.value):
                    traffic = traffic_agents.pop(0)
                    self.used_traffics.append(traffic[0])

                    agent = TrafficLightAgent(traffic[0], traffic[1], self, (i, j))
                    await agent.start()

                    self.city_schema[i][j] = agent.my_behav
                    agents.append(agent.my_behav)

                    continue
                self.city_schema[i][j] = TYPE(content[i][j])

        console.addstr("Configuring traffic lights...\n")
        console.refresh()
        await asyncio.sleep(1)
        for agent in agents:
            agent.configure_traffic_light()


    def update_city(self, car: CarAgent) -> None:
        position: List[int] = car.get_position()
        name: str = car.get_name()

        for i in range(self.city_height):
            for j in range(self.city_width):
                if (self.city[i][j] == None): continue
                if (self.city[i][j].get_name() == name): 
                    self.city[i][j] = None
                    break

        self.city[position[0]][position[1]] = car

    def print_city(self) -> None:
        stdscr.scrollok(True)

        while True:
            city.clear()

            for i in range(self.city_height):
                for j in range(self.city_width):
                    if isinstance(self.city[i][j], CarAgent.behav): 
                        car: Tuple[str, COLORS] = self.city[i][j].get_arrow()
                        city.addch(car[0], curses.color_pair(car[1].value))
                        continue

                    if isinstance(self.city_schema[i][j], TrafficLightAgent.behav):
                        traffic: Tuple[str, COLORS] = self.city_schema[i][j].get_character()
                        city.addch(traffic[0], curses.color_pair(traffic[1].value))
                        continue

                    city.addch(self.city_schema[i][j].value)

                city.addch('\n')

            city.refresh()
            console.refresh()
            clock.refresh()
            time.sleep(1 / SIMULATION_SPEED)

