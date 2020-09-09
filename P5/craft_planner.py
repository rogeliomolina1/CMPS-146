import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
#added those seen below
from math import inf
from heapq import heappop, heappush


#Partner was ALex Perrotti


Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.

    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        if 'Requires' in rule:
            for requirement in rule['Requires']:
                if not state[requirement]:
                    return False
        if 'Consumes' in rule:
            for consumable in rule['Consumes']:
                if not state[consumable] >= rule['Consumes'][consumable]:
                    return False
        return True

    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # next_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = state.copy()
        if 'Consumes' in rule:
            for consumable in rule['Consumes']:
                next_state[consumable] -= rule['Consumes'][consumable]
        if 'Produces' in rule:
            for product in rule['Produces']:
                next_state[product] += rule['Produces'][product]
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        for condition in goal:
            if not state[condition] >= goal[condition]:
                return False
        return True

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(state):
    # Implement your heuristic here!
    if state['wood'] > 1 or state['plank'] > 7 or state['stick'] > 5 or state['bench'] > 1 or state['wooden_axe'] > 0 or state['wooden_pickaxe'] > 1 or state['cobble'] > 8 or state['coal'] > 1 or state['stone_axe'] > 0 or state['stone_pickaxe'] > 1 or state['ore'] > 1 or state['furnace'] > 1 or state['ingot'] > 6 or state['iron_axe'] > 0 or state['iron_pickaxe'] > 1:
        #avoid having more than you'll ever need of something
        #conditional is ordered by likelyhood as to check faster
        return inf
    return 0

def search(graph, state, is_goal, limit, heuristic):

    start_time = time()

    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state

    #normal A* structures
    path = []
    queue = [(0, state)]
    #pair: (previous state, action taken from that state)
    prev_pairs = {}
    prev_pairs[state] = None
    #total recipe time
    costs = {}
    costs[state] = 0
    #total number of steps
    steps = {}
    steps[state] = 0

    while time() - start_time < limit:
        current_cost, current_state = heappop(queue)
        if is_goal(current_state):
            print("Time:", (time() - start_time))
            print("Cost:", costs[current_state])
            print("Len:", steps[current_state])
            #fill path with (state, action to that state) pairs
            while prev_pairs[current_state]:
                prev_state, prev_action = prev_pairs[current_state]
                path.append((current_state, prev_action))
                current_state = prev_state
            path.reverse()
            return path
        #act_ is short for action, as graph(state) generates possible actions
        for act_name, act_state, act_cost in graph(current_state):
            # the +1 is a len counter (number of steps)
            pathcost = current_cost + act_cost
            pathlen = steps[current_state] + 1
            #only considers pathcost, but prints steps at the end
            if act_state not in costs or pathcost < costs[act_state]:
                costs[act_state] =  current_cost + act_cost
                steps[act_state] = pathlen
                prev_pairs[act_state] = (current_state, (act_name, act_state, act_cost))
                heappush(queue, (heuristic(act_state) + pathcost, act_state))

    # Failed to find a path
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    print("final state = ", current_state)#test
    return None

if __name__ == '__main__':
    with open('crafting.json') as f:
        Crafting = json.load(f)

    # # List of items that can be in your inventory:
    #print('All items:', Crafting['Items'])
    #
    # # List of items in your initial inventory with amounts:
    print('Initial inventory:', Crafting['Initial'])
    #
    # # List of items needed to be in your inventory at the end of the plan:
    print('Goal:',Crafting['Goal'])
    #
    # # Dict of crafting recipes (each is a dict):
    #print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])

    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 30, heuristic)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t',state)
            print(action)
