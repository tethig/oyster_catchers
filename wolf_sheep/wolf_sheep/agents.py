import random

from mesa import Agent

from wolf_sheep.gaussian_walk import RandomWalker


class OysterCatcher(RandomWalker):
    '''
    An oystercatcher that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    '''

    energy = None

    def __init__(self, pos, model, sigma=2, energy=None):
        super().__init__(pos, model, sigma=2) # do I need sigma=2?
        self.energy = energy

    def step(self):
        '''
        A model step. Move, then eat grass and reproduce.
        '''
        self.gaussian_move()
        living = True

        # Reduce energy
        self.energy -= 1

        # If there is grass available, eat it
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        grass_patch = [obj for obj in this_cell
                       if isinstance(obj, GrassPatch)][0]
        if grass_patch.fully_grown:
            self.energy += self.model.oystercatcher_gain_from_food
            grass_patch.fully_grown = False

        # Death
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        if living and random.random() < self.model.oystercatcher_reproduce:
            # Create a new oystercatcher:
            self.energy /= 2
            chick = OysterCatcher(self.pos, self.model, self.sigma, self.energy)
            self.model.grid.place_agent(chick, self.pos)
            self.model.schedule.add(chick)

class GrassPatch(Agent):
    '''
    A patch of grass that grows at a fixed rate and it is eaten by oystercatcher
    '''

    def __init__(self, pos, model, fully_grown, countdown):
        '''
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        '''
        super().__init__(pos, model)
        self.fully_grown = fully_grown
        self.countdown = countdown

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1
