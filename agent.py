import random
import heapq
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
    def __init__(self):
        self.plan = []
        self.active_algo = 'BFS'

    def sense_and_act(self, percept: dict) -> str:
        # If plan is empty, find closest food and compute offline plan
        if not self.plan:
            all_food = percept.get('all_food', [])
            if not all_food:
                return 'Stay'

            agent_pos = tuple(percept.get('agent_pos', [0, 0]))
            walls = percept.get('walls', [])
            grid_size = percept.get('grid_size', (10, 10))

            # Find closest food pellet by Manhattan distance
            closest_food = min(
                all_food,
                key=lambda f: abs(agent_pos[0] - f[0]) + abs(agent_pos[1] - f[1])
            )

            # Run active search algorithm
            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(agent_pos, closest_food, walls, grid_size) or []
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(agent_pos, closest_food, walls, grid_size) or []
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(agent_pos, closest_food, walls, grid_size) or []

        if self.plan:
            return self.plan.pop(0)
        return 'Stay'

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        start = tuple(start_pos)
        goal = tuple(goal_pos)
        walls_set = set(tuple(w) for w in walls)
        width, height = grid_size

        queue = deque([(start, [])])
        reached = {start}

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
                    next_pos not in reached):
                    reached.add(next_pos)
                    queue.append((next_pos, path + [action]))

        return None

    def dfs_search(self, start_pos, goal_pos, walls, grid_size):
        start = tuple(start_pos)
        goal = tuple(goal_pos)
        walls_set = set(tuple(w) for w in walls)
        width, height = grid_size

        stack = [(start, [])]
        reached = {start}

        moves = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0))
        ]

        while stack:
            current, path = stack.pop()
            if current == goal:
                return path

            for action, (dx, dy) in moves:
                next_pos = (current[0] + dx, current[1] + dy)
                if (0 <= next_pos[0] < width and
                    0 <= next_pos[1] < height and
                    next_pos not in walls_set and
                    next_pos not in reached):
                    reached.add(next_pos)
                    stack.append((next_pos, path + [action]))

        return None

    def ucs_search(self, start_pos, goal_pos, walls, grid_size):
        start = tuple(start_pos)
        goal = tuple(goal_pos)
        walls_set = set(tuple(w) for w in walls)
        width, height = grid_size

        counter = 0
        pq = [(0, counter, start, [])]
        reached = {start: 0}

        moves = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0))
        ]

        while pq:
            cost, _, current, path = heapq.heappop(pq)
            if current == goal:
                return path

            for action, (dx, dy) in moves:
                next_pos = (current[0] + dx, current[1] + dy)
                new_cost = cost + 1
                if (0 <= next_pos[0] < width and
                    0 <= next_pos[1] < height and
                    next_pos not in walls_set):
                    if next_pos not in reached or new_cost < reached[next_pos]:
                        reached[next_pos] = new_cost
                        counter += 1
                        heapq.heappush(pq, (new_cost, counter, next_pos, path + [action]))

        return None