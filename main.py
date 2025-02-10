from renderer import Renderer
from simulation import Simulation

if __name__=="__main__":
    simulation=Simulation()
    renderer=Renderer(simulation)
    while True:
        renderer.render()
