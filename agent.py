import random
import heapq
import math
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
        self.active_algo = 'AStar'

    def manhattan_distance(self, pos, goal):
        return int(abs(pos[0] - goal[0]) + abs(pos[1] - goal[1]))

    def euclidean_distance(self, pos, goal):
        return float(math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2))

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
                key=lambda f: self.manhattan_distance(agent_pos, f)
            )

            # Run active search algorithm
            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(agent_pos, closest_food, walls, grid_size) or []
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(agent_pos, closest_food, walls, grid_size) or []
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(agent_pos, closest_food, walls, grid_size) or []
            elif self.active_algo == 'AStar':
                self.plan = self.astar_search(agent_pos, closest_food, walls, grid_size) or []

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

    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        start = tuple(start_pos)
        goal = tuple(goal_pos)
        walls_set = set(tuple(w) for w in walls)
        width, height = grid_size

        pq = []
        reached_states = set()

        # Calculate initial heuristic
        if heuristic_type == 'euclidean':
            h_start = self.euclidean_distance(start, goal)
        else:
            h_start = self.manhattan_distance(start, goal)

        # Priority queue tuple: (f_cost, g_cost, current_pos, path_taken)
        heapq.heappush(pq, (h_start, 0, start, []))

        moves = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0))
        ]

        while pq:
            f_cost, g_cost, current_pos, path_taken = heapq.heappop(pq)

            if current_pos == goal:
                return path_taken

            if current_pos in reached_states:
                continue
            reached_states.add(current_pos)

            for action, (dx, dy) in moves:
                neighbor = (current_pos[0] + dx, current_pos[1] + dy)
                if (0 <= neighbor[0] < width and
                    0 <= neighbor[1] < height and
                    neighbor not in walls_set and
                    neighbor not in reached_states):
                    g_new = g_cost + 1
                    if heuristic_type == 'euclidean':
                        h_new = self.euclidean_distance(neighbor, goal)
                    else:
                        h_new = self.manhattan_distance(neighbor, goal)
                    f_new = g_new + h_new
                    heapq.heappush(pq, (f_new, g_new, neighbor, path_taken + [action]))

        return None