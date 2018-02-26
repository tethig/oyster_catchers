#!/usr/bin/env python

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from model import ForageModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if agent.reserve > 5:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 11, 500, 500)
chart = ChartModule([{"Label": "gini",
                      "Color": "Black"}],
                    data_collector_name='dc')

server = ModularServer(ForageModel,
                       [grid, chart],
                       name="OysterCatcher Model",
                       model_params={"n_agents": 15, "width": 10, "height": 11})
server.launch()
