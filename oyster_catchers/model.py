'''
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
'''

# Import modules
import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from oyster_catchers.agents import OysterCatcher, Limpet
from oyster_catchers.schedule import RandomActivationByBreed


class OysterCatcherForaging(Model):
    '''
    OysterCatcher Foraging Model
    '''

    width = 50
    height = 30

    sigma = 2
    initial_oystercatchers = 100
    oystercatcher_reproduce = 0.04
    initial_limpets = 1000
    limpet_regrowth_time = 30
    oystercatcher_gain_from_food = 4

    verbose = False  # Print-monitoring

    description = 'A model for simulating oystercatcher movement and feeding.'

    def __init__(self, width=50, height=30, sigma=2,
                 initial_oystercatchers=100,
                 oystercatcher_reproduce=0.04,
                 initial_limpets=1000,
                 limpet_regrowth_time=30, oystercatcher_gain_from_food=4):
        '''
        Create a new OysterCatcher Foraging model with the given parameters.

        Args:
            sigma: Movement sigma for oystercatcher dispersal
            initial_oystercatchers: Number of oystercatchers to start with
            oystercatcher_reproduce: Probability of each oystercatcher reproducing each step
            limpet_regrowth_time: How long it takes for a limpet to regrow once it is eaten
            oystercatcher_gain_from_food: Energy oystercatchers gain from limpets
        '''

        # Set parameters
        self.width = width
        self.height = height
        self.sigma = sigma
        self.initial_oystercatchers = initial_oystercatchers
        self.oystercatcher_reproduce = oystercatcher_reproduce
        self.limpet_regrowth_time = limpet_regrowth_time
        self.oystercatcher_gain_from_food = oystercatcher_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.width, self.height, torus=True) #### previously height then width!!!!
        self.datacollector = DataCollector(
            {"OysterCatcher": lambda m: m.schedule.get_breed_count(OysterCatcher),
            "Limpet": lambda m: m.schedule.get_breed_count(Limpet)})

        # Create oystercatchers:
        for i in range(self.initial_oystercatchers):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = random.randrange(2 * self.oystercatcher_gain_from_food)
            oystercatcher = OysterCatcher((x, y), self, sigma, energy)
            self.grid.place_agent(oystercatcher, (x, y))
            self.schedule.add(oystercatcher)

        # Create limpets
        for i in range(self.initial_limpets):
            x = random.randrange(self.width)
            y = random.randrange(self.height)

            fully_grown = random.choice([True, False])
            if fully_grown:
                countdown = self.limpet_regrowth_time
            else:
                countdown = random.randrange(self.limpet_regrowth_time)

            limpet = Limpet((x, y), self, fully_grown, countdown)
            self.grid.place_agent(limpet, (x, y))
            self.schedule.add(limpet)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                self.schedule.get_breed_count(OysterCatcher),
                self.schedule.get_breed_count(Limpet)])

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number limpets: ',
                self.schedule.get_breed_count(Limpet))
            print('Initial number oystercatchers: ',
                self.schedule.get_breed_count(OysterCatcher))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number limpets: ',
                self.schedule.get_breed_count(Limpet))
            print('Final number sheep: ',
                self.schedule.get_breed_count(OysterCatcher))
