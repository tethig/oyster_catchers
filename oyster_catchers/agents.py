# Import modules
import random
from mesa import Agent
from oyster_catchers.gaussian_walk import RandomWalker

# Agent classes
class OysterCatcher(RandomWalker):
    '''
    An oystercatcher that walks around and reproduces asexually.
    The init is the same as the RandomWalker.
    '''

    energy = None

    def __init__(self, pos, model, sigma=2, energy=None):
        super().__init__(pos, model)
        self.sigma = sigma
        self.energy = energy

    def step(self):
        '''
        A model step. Move, then eat limpet and reproduce.
        '''
        self.gaussian_move()
        living = True

        # Reduce energy
        self.energy -= 1

        # If there is a limpet available, eat it
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        limpets = [obj for obj in this_cell if isinstance(obj, Limpet)]
        if len(limpets) > 0:
            limpet_to_eat = random.choice(limpets)
            if limpet_to_eat.fully_grown:
                self.energy += self.model.oystercatcher_gain_from_food
                limpet_to_eat.fully_grown = False

        # Death
        if self.energy <= 0: # was previous less than only
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        if living and random.random() < self.model.oystercatcher_reproduce:
            # Create a new oystercatcher:
            self.energy /= 2
            chick = OysterCatcher(self.pos, self.model, self.sigma, self.energy)
            self.model.grid.place_agent(chick, self.pos)
            self.model.schedule.add(chick)

class Limpet(Agent):
    '''
    A limpet that grows at a fixed rate and it is eaten by oystercatcher
    '''

    def __init__(self, pos, model, fully_grown, countdown):
        '''
        Creates a new limpet
        Args:
            grown: (boolean) Whether the limpet is fully grown or not
            countdown: Time for the limpet to be fully grown again
        '''
        super().__init__(pos, model)
        self.fully_grown = fully_grown
        self.countdown = countdown

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.limpet_regrowth_time
            else:
                self.countdown -= 1
