#!/usr/bin/env python

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
import random

class OysterCatcher(Agent):
    """ A foraging agent with initial reserve."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.reserve = 100

    def move(self):
        x, y = self.pos

        dx = 1 + int( random.expovariate(lambd=1) ) # see section 2; is there a better one?
        dy = 1 + int( random.expovariate(lambd=1) )

        if random.randint(0,1):
            dx = - dx
        if random.randint(0,1):
            dy = - dy
        #possible_steps = self.model.grid.get_neighborhood(
        #    self.pos,
        #    moore=True, # Moore setting means diagnonals can be used too
        #    include_center=False, radius=radius) # centre won't be revisited; radius sets distance travelled
        #new_position = random.choice(possible_steps) # so even if distant sites are included you may end up close
        new_position = (x + dx, y + dy) # what if we go over perimeter? set toroidal for now
        self.model.grid.move_agent(self, new_position)

    def donate_reserve(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = random.choice(cellmates)
            other.reserve += int(self.reserve / 2) # approximately half given away
            self.reserve -= int(self.reserve / 2)

    def step(self):
        self.move()
        if self.reserve > 0:
            self.donate_reserve()

## Thoughts: could have limpets as agents
## Seems easier to have them as simplest possible representation
## Perhaps distribute M limpet agents in the ForageModel during __init__
## For eating (to replace donate_reserve()) we then need method for looking at limpets only

def compute_gini(model):
    agent_wealths = [agent.reserve for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum( xi * (N-i) for i,xi in enumerate(x) ) / (N*sum(x))
    return (1 + (1/N) - 2*B)

class ForageModel(Model):
    """A model with some number of agents."""
    def __init__(self, n_agents, width, height):
        self.running = True # this was important for visualization
        self.num_agents = n_agents
        self.grid = MultiGrid(width, height, torus=True) # True means toroidal space (for now)
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            a = OysterCatcher(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            coords = (random.randrange(self.grid.width), random.randrange(self.grid.height))
            self.grid.place_agent(a, coords)

        self.dc = DataCollector(
            model_reporters={"agent_count": lambda m: m.schedule.get_agent_count() , "gini": compute_gini},
            agent_reporters={"name": lambda a: a.unique_id , "reserve": lambda a: a.reserve}
        )

    def step(self):
        '''Advance the model by one step.'''
        self.dc.collect(self)
        self.schedule.step()
