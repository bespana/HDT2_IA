import numpy as np
import random
from enum import IntEnum

class Action(IntEnum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3

class FrozenLake:
    def __init__(self, start=(0, 0), goal=(3, 3), seed=42):
        self.start = start
        self.goal = goal
        self.state = start
        self.grid_size = 4
        self.holes = self.generate_holes(seed)
        self.actions = [Action.UP, Action.DOWN, Action.RIGHT, Action.LEFT]
        
    def generate_holes(self, seed):
        random.seed(seed)
        holes = set()
        num_holes = random.randint(1, 3)
        while len(holes) < num_holes:
            hole = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
            if hole != self.start and hole != self.goal:
                holes.add(hole)
        return holes

    def reset(self):
        self.state = self.start
        return self.state

    def step(self, action):
        if action == Action.UP:
            next_state = (max(0, self.state[0]-1), self.state[1])
        elif action == Action.DOWN:
            next_state = (min(self.grid_size-1, self.state[0]+1), self.state[1])
        elif action == Action.RIGHT:
            next_state = (self.state[0], min(self.grid_size-1, self.state[1]+1))
        elif action == Action.LEFT:
            next_state = (self.state[0], max(0, self.state[1]-1))
        
        if next_state in self.holes:
            reward = -1
            done = True
        elif next_state == self.goal:
            reward = 1
            done = True
        else:
            reward = 0
            done = False
        
        self.state = next_state
        return next_state, reward, done

    def render(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (i, j) == self.state:
                    print("S", end=" ")
                elif (i, j) == self.goal:
                    print("G", end=" ")
                elif (i, j) in self.holes:
                    print("H", end=" ")
                else:
                    print("F", end=" ")
            print()
        print()

# Example usage
lake = FrozenLake()
lake.render()

# Simple policy: always move right until it's not possible, then move down
def simple_policy(state):
    if state[1] < lake.grid_size - 1:
        return Action.RIGHT
    else:
        return Action.DOWN

# Run policy
state = lake.reset()
done = False
while not done:
    action = simple_policy(state)
    state, reward, done = lake.step(action)
    lake.render()

