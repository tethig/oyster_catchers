'''
Generalized behavior for random walking, one grid cell at a time.
'''

# Import modules
import random
from mesa import Agent

# Agent class
class RandomWalker(Agent):
    '''
    Parent class for moving agent.
    '''

    grid = None
    x = None
    y = None
    sigma = 2

    def __init__(self, pos, model, sigma=2):
        '''
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        sigma: deviation from home square
        '''
        super().__init__(pos, model)
        self.pos = pos
        self.sigma = 2

    def gaussian_move(self):
        '''
        Gaussian step in any allowable direction.
        '''
        x, y = self.pos
        coord = (x, y)
        while coord == self.pos:
            dx, dy = int(random.gauss(0, self.sigma)), int(random.gauss(0, self.sigma))
            coord = (x + dx, y + dy)

        # Now move:
        self.model.grid.move_agent(self, coord)
