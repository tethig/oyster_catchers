'''
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
'''

import random

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from wolf_sheep.agents import OysterCatcher, GrassPatch
from wolf_sheep.schedule import RandomActivationByBreed


class WolfSheepPredation(Model):
    '''
    Wolf-Sheep Predation Model
    '''

    height = 20
    width = 20

    initial_oystercatchers = 100

    oystercatcher_reproduce = 0.04

    grass = False
    grass_regrowth_time = 30
    oystercatcher_gain_from_food = 4

    verbose = False  # Print-monitoring

    description = 'A model for simulating wolf and sheep (predator-prey) ecosystem modelling.'

    def __init__(self, height=20, width=20,
                 initial_oystercatchers=100,
                 oystercatcher_reproduce=0.04,
                 grass=False, grass_regrowth_time=30, oystercatcher_gain_from_food=4):
        '''
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_oystercatchers: Number of sheep to start with
            oystercatcher_reproduce: Probability of each sheep reproducing each step
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            oystercatcher_gain_from_food: Energy sheep gain from grass, if enabled.
        '''

        # Set parameters
        self.height = height
        self.width = width
        self.initial_oystercatchers = initial_oystercatchers
        self.oystercatcher_reproduce = oystercatcher_reproduce
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.oystercatcher_gain_from_food = oystercatcher_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {"OysterCatcher": lambda m: m.schedule.get_breed_count(OysterCatcher),
            "Grass": lambda m: m.schedule.get_breed_count(GrassPatch)})

        # Create sheep:
        for i in range(self.initial_oystercatchers):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = random.randrange(2 * self.oystercatcher_gain_from_food)
            oystercatcher = OysterCatcher((x, y), self, True, energy)
            self.grid.place_agent(oystercatcher, (x, y))
            self.schedule.add(oystercatcher)

        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = random.randrange(self.grass_regrowth_time)

                patch = GrassPatch((x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                self.schedule.get_breed_count(OysterCatcher),
                self.schedule.get_breed_count(GrassPatch)])

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number limpets: ',
                self.schedule.get_breed_count(GrassPatch))
            print('Initial number sheep: ',
                self.schedule.get_breed_count(OysterCatcher))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number limpets: ',
                self.schedule.get_breed_count(GrassPatch))
            print('Final number sheep: ',
                self.schedule.get_breed_count(OysterCatcher))
