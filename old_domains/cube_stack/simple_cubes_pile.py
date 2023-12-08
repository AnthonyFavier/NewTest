import hatpehda
from copy import deepcopy

from typing import Dict

"""
Simple domain where a robot and a human have 3 different numbered cube each. They must build a 3 block height stack without 
specific order.
Result : 
Plan : [('robot_pick', 'cube4'), ('robot_stack',), ('human_pick', 'cube1'), ('human_stack',), ('human_pick', 'cube2'), ('human_stack',)]
"""

### Operators definition

def human_pick(agents, self_state, self_name, c):
    if self_name in self_state.isReachableBy[c] and self_state.isCarrying[self_name] is None:
        for a in agents.values():
            a.state.isReachableBy[c] = []
            # should check if agent is in the same piece... Observability of action ?
            # Can put in other agent head that he saw me executing or just the facts (the human has done it, or just it is done)
            a.state.isCarrying[self_name] = c
        return agents
    else:
        return False


def robot_pick(agents: Dict[str, hatpehda.Agent], self_state, self_name, c):
    if self_name in self_state.isReachableBy[c] and self_state.isCarrying[self_name] is None:
        for a in agents.values():
            a.state.isReachableBy[c] = []
            # should check if agent is in the same piece... Observability of action ?
            a.state.isCarrying[self_name] = c
        return agents
    else:
        return False


def human_stack(agents, self_state, self_name):
    if self_state.isCarrying[self_name] is not None:
        c = self_state.isCarrying[self_name]
        for a in agents.values():
            a.state.isOnStack[c] = True
            a.state.isCarrying[self_name] = None
        return agents
    else:
        return False


def robot_stack(agents, self_state, self_name):
    if self_state.isCarrying[self_name] is not None:
        c = self_state.isCarrying[self_name]
        for a in agents.values():
            a.state.isOnStack[c] = True
            a.state.isCarrying[self_name] = None
        return agents
    else:
        return False


hatpehda.declare_operators("human", human_pick, human_stack)
hatpehda.declare_operators("robot", robot_pick, robot_stack)

### Methods definitions

def moveb_m_human(agents, self_state, self_name, c, goal):
    if self_name in self_state.isReachableBy[c] and c in goal.isOnStack and goal.isOnStack[c] and not self_state.isOnStack[c]:
        return [("human_pick", c), ("human_stack",)]
    return []

def moveb_m_robot(agents, self_state: hatpehda.State, self_name, c, goal):
    if self_name in self_state.isReachableBy[c] and c in goal.isOnStack and goal.isOnStack[c] and not self_state.isOnStack[c]:
            return [("robot_pick", c), ("robot_stack",)]
    return []

def stack_human(agents, self_state, self_name, goal):
    for c in self_state.cubes:
        if self_name in self_state.isReachableBy[c] and c in goal.isOnStack and goal.isOnStack[c] and not self_state.isOnStack[c]:
            return [("move_one", c, goal), ("stack", goal)]
    return []

def stack_robot(agents, self_state, self_name, goal):
    for c in self_state.cubes:
        if self_name in self_state.isReachableBy[c] and c in goal.isOnStack and goal.isOnStack[c] and not self_state.isOnStack[c]:
            return [("move_one", c, goal), ("stack", goal)]
    return []

hatpehda.declare_methods("human", "move_one", moveb_m_human)
hatpehda.declare_methods("robot", "move_one", moveb_m_robot)
hatpehda.declare_methods("human", "stack", stack_human)
hatpehda.declare_methods("robot", "stack", stack_robot)

hatpehda.print_operators()

hatpehda.print_methods()


def make_reachable_by(state, cubes, agent):
    if not hasattr(state, "isReachableBy"):
        state.isReachableBy = {}
    state.isReachableBy.update({c: agent for c in cubes})

def put_on_stack(state, cubes, is_stacked):
    if not hasattr(state, "isOnStack"):
        state.isOnStack = {}
    state.isOnStack.update({c: is_stacked for c in cubes})


state1_h = hatpehda.State("state1_h")
state1_h.cubes = ["cube1", "cube2", "cube3", "cube4", "cube5", "cube6"]
make_reachable_by(state1_h, state1_h.cubes[:3], ["human"])
make_reachable_by(state1_h, state1_h.cubes[3:], ["robot"])
put_on_stack(state1_h, state1_h.cubes, False)
state1_h.isCarrying = {"human": None, "robot": None}

state1_r = deepcopy(state1_h)

goal1_h = hatpehda.Goal("goal1_h")
goal1_h.isOnStack = {"cube1": True, "cube2": True, "cube4": True}
goal1_r = deepcopy(goal1_h)

hatpehda.set_state("human", state1_h)
hatpehda.add_tasks("human", [('stack', goal1_h)])
hatpehda.set_state("robot", state1_r)
hatpehda.add_tasks("robot", [('stack', goal1_r)])

hatpehda.print_state(hatpehda.agents["human"].state)

sol = []
plans = hatpehda.seek_plan_robot(hatpehda.agents, "robot", sol)

for agents in sol:
    for name, a in agents.items():
        print(name, "plan:", a.plan)
    print("######")



