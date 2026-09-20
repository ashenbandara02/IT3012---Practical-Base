import random
from collections import deque


class GreedyGridAgent:
    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    def sense_and_act(self, percept: dict) -> str:
        # Condition-action rules
        if percept.get('food_here'):
            return 'Up'
        if percept.get('wall_ahead'):
            return 'Left'
        return 'Up'


class ModelBasedAgent:
    def __init__(self):
        # Internal state memory
        self.last_action = None
        self.last_percept = None

    def sense_and_act(self, percept: dict) -> str:
        wall_ahead = percept.get('wall_ahead', False)
        food_here = percept.get('food_here', False)

        # Condition-action rules querying memory
        if food_here:
            action = self.last_action if self.last_action else 'Up'
        elif wall_ahead:
            # Change action if stuck in a loop
            if self.last_action == 'Left':
                action = 'Right'
            elif self.last_action == 'Right':
                action = 'Down'
            elif self.last_action == 'Down':
                action = 'Up'
            else:
                action = 'Left'
        else:
            action = self.last_action if self.last_action else 'Up'

        # Update state (transition and sensor model)
        self.last_action = action
        self.last_percept = percept
        return action


class SearchAgent:
    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        start = tuple(start_pos)
        goal = tuple(goal_pos)
        walls_set = set(tuple(w) for w in walls)
        width, height = grid_size

        queue = deque([(start, [])])
        visited = {start}

        moves = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0))
        ]

        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path

            for action, (dx, dy) in moves:
                next_pos = (current[0] + dx, current[1] + dy)
                if (0 <= next_pos[0] < width and
                    0 <= next_pos[1] < height and
                    next_pos not in walls_set and
                    next_pos not in visited):
                    visited.add(next_pos)
                    queue.append((next_pos, path + [action]))

        return None