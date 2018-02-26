# Import modules
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from oyster_catchers.agents import OysterCatcher, Limpet
from oyster_catchers.model import OysterCatcherForaging


def oystercatcher_limpet_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is OysterCatcher:
        portrayal["Shape"] = "oyster_catchers/resources/bird.png"
        # https://icons8.com/icon/50494/bird
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Limpet:
        if agent.fully_grown:
            portrayal["Shape"] = "wolf_sheep/resources/limpet.png"
            # https://icons8.com/icon/37550/shellfish
        else:
            # portrayal["Color"] = "#ffffff"
            portrayal["Shape"] = "rect"
        # portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        # portrayal["w"] = 1
        # portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(oystercatcher_limpet_portrayal, 50, 30, 800, 480) # width then height!!!!!!!
chart_element = ChartModule([{"Label": "OysterCatcher", "Color": "#AA0000"},
                             {"Label": "Limpet", "Color": "#666666"}])

model_params = {"sigma": UserSettableParameter('slider', 'Movement sigma', 2, 1, 5),
                "initial_oystercatchers": UserSettableParameter('slider', 'Initial OysterCatcher Population', 100, 10, 300),
                "oystercatcher_reproduce": UserSettableParameter('slider', 'OysterCatcher Reproduction Rate', 0.04, 0.01, 1.0, 0.01),
                "limpet_regrowth_time": UserSettableParameter('slider', 'Limpet Regrowth Time', 30, 1, 100),
                "oystercatcher_gain_from_food": UserSettableParameter('slider', 'OysterCatcher Gain From Food', 4, 1, 10)}

server = ModularServer(OysterCatcherForaging, [canvas_element, chart_element], "OysterCatcher Foraging", model_params)
server.port = 8521
