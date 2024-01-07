import asyncio
import curses
from traffic_light import TrafficLightAgent
from car import CarAgent
import time
from header import city, stdscr, logs, COLORS, TYPE

class Environment:
    def get_agent(self, position):
        if isinstance(self.city[position[0]][position[1]], CarAgent.behav):
            return self.city[position[0]][position[1]].name
        elif isinstance(self.city_schema[position[0]][position[1]], TrafficLightAgent.behav): 
            return self.city_schema[position[0]][position[1]].name
        else:
            return None

    async def generate(self):
        agents = []
        file = open("map.txt", "r")
        content = file.readlines()
        agent_count = 0

        self.used_traffics = []
        self.city_height = len(content)
        self.city_width = len(content[0]) - 1
        self.city_schema = [[TYPE.ROAD for i in range(self.city_width)] for j in range(self.city_height)]
        self.city = [[None for i in range(self.city_width)] for j in range(self.city_height)]
        
        for i in range(self.city_height):
            for j in range(self.city_width):
                if (content[i][j] == TYPE.LIGHT.value):
                    agent_count += 1
                    agent = f"traffic{agent_count}@localhost"
                    self.used_traffics.append(agent)

                    agent = TrafficLightAgent(agent, "traffic", self, (i, j))
                    await agent.start()

                    self.city_schema[i][j] = agent.my_behav
                    agents.append(agent.my_behav)

                    continue
                self.city_schema[i][j] = TYPE(content[i][j])

        await asyncio.sleep(2)
        for agent in agents:
            agent.configure_traffic_light()


    def update_city(self, car):
        position = car.position
        name = car.name

        for i in range(self.city_height):
            for j in range(self.city_width):
                if (self.city[i][j] == None): continue
                if (self.city[i][j].name == name): 
                    self.city[i][j] = None
                    break

        self.city[position[0]][position[1]] = car

    def print_city(self):
        stdscr.scrollok(True)

        while True:
            city.clear()

            for i in range(self.city_height):
                for j in range(self.city_width):
                    if isinstance(self.city[i][j], CarAgent.behav): 
                        city.addch("*", curses.color_pair(COLORS.RED.value if self.city[i][j].urgent else COLORS.WHITE.value))
                    elif isinstance(self.city_schema[i][j], TrafficLightAgent.behav):
                        city.addch("+", curses.color_pair(self.city_schema[i][j].light.value))
                    else:
                        city.addch(self.city_schema[i][j].value)
                city.addch('\n')

            city.refresh()
            logs.refresh()
            time.sleep(0.25)

