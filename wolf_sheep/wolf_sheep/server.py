from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from wolf_sheep.agents import OysterCatcher, GrassPatch
from wolf_sheep.model import WolfSheepPredation


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is OysterCatcher:
        portrayal["Shape"] = "wolf_sheep/resources/bird.png"
        # https://icons8.com/web-app/433/sheep
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Shape"] = "wolf_sheep/resources/limpet.png"
        else:
            portrayal["Color"] = "#ffffff"
            portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule([{"Label": "OysterCatcher", "Color": "#AA0000"},
                             {"Label": "GrassPatch", "Color": "#666666"}])

model_params = {"grass": UserSettableParameter('checkbox', 'Grass Enabled', True),
                "grass_regrowth_time": UserSettableParameter('slider', 'Grass Regrowth Time', 20, 1, 100),
                "initial_oystercatchers": UserSettableParameter('slider', 'Initial OysterCatcher Population', 100, 10, 300),
                "oystercatcher_reproduce": UserSettableParameter('slider', 'OysterCatcher Reproduction Rate', 0.04, 0.01, 1.0,
                                                         0.01),
                "oystercatcher_gain_from_food": UserSettableParameter('slider', 'OysterCatcher Gain From Food', 4, 1, 10)}

server = ModularServer(WolfSheepPredation, [canvas_element, chart_element], "Wolf Sheep Predation", model_params)
server.port = 8521
