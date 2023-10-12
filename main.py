import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from spade import wait_until_finished


from traffic_light import TrafficLightAgent

async def main():
#    dummy = DummyAgent("admin@localhost", "password")
#    await dummy.start()
#
#    # wait until user interrupts with ctrl+C
#    while not dummy.my_behav.is_killed():
#        try:
#            await asyncio.sleep(1)
#        except KeyboardInterrupt:
#            break
#
#    assert dummy.my_behav.exit_code == 10
#
#    await dummy.stop()

    light = TrafficLightAgent("admin@localhost", "password")
    await light.start()
    await wait_until_finished(light)
    print("\t\ta")


if __name__ == "__main__":
        spade.run(main())

