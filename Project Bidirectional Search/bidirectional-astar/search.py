# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import searchAgents

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    actions = []
    closed = set()          # nodes that already passed by
    parents = dict()        # parent of a node
    fringe = util.Stack()   # DFS queue
    fringe.push([[problem.getStartState(), None, None], None])     # [[pos, direction, cost], parent]

    while fringe.isEmpty() == False:
        [node, parent] = fringe.pop()        # node = [state, direction, cost]
        parents[node[0]] = parent

        # check if pos is the goal
        if problem.isGoalState(node[0]):

            # Find the goal! Trace back the action path
            curr = node
            while curr[0] != problem.getStartState():   # loop from goal to the start
                parent = parents[curr[0]]               # get the parent of current state from dictionary
                actions.append(curr[1])                 # store the action to the list, which is one of 'North', 'West', 'East', or 'South'
                curr = parent

            actions.reverse()   # reverse the action list to start in the start state
            return actions

        # push state to the closed set, so that we don't have to expand children again
        closed.add(node[0])

        # push the child of the node to the stack
        for successor in problem.getSuccessors(node[0]):
            # successor format: ((34, 15), 'South', 1)
            if (successor[0] in closed) == False:
                fringe.push([successor, node])    # [child, parent]

    print("Failed. Unable to find the goal!")
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    actions = []
    closed = set()          # nodes that already passed by
    parents = dict()        # parent of a node
    fringe = util.Queue()    # BFS queue
    fringe.push([[problem.getStartState(), None, None], None])     # [[pos, direction, cost], parent]

    while fringe.isEmpty() == False:
        [node, parent] = fringe.pop()        # node = [state, direction, cost]

        # if we already expand this node, skip this
        if (node[0] in closed) == True:
            continue
        
        # push state to the closed set, so that we don't have to expand children again
        closed.add(node[0])

        # record the parent pos of this pos
        parents[node[0]] = parent

        # check if pos is the goal
        if problem.isGoalState(node[0]):

            # Success! Find the goal! construct action path
            curr = node
            while curr[0] != problem.getStartState():   # loop from goal to the start
                parent = parents[curr[0]]               # get the parent of current state from dictionary
                actions.append(curr[1])                 # store the action to the list, which is one of 'North', 'West', 'East', or 'South'
                curr = parent

            actions.reverse()   # reverse the action list to start in the start state
            return actions

        # push the child of the node to the queue
        for successor in problem.getSuccessors(node[0]):
            # successor format: ((34, 15), 'South', 1)
            fringe.push([successor, node])    # [child, parent]

    print("Failed. Unable to find the goal!")
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    actions = []
    closed = set()                  # nodes that already passed by
    parents = dict()                # parent of a node
    fringe = util.PriorityQueue()   # priority queue
    fringe.push([[problem.getStartState(), None, 0], None, 0], 0)     # ([[pos, direction, cost], parent, cumulative_cost], cumulative_cost)

    while fringe.isEmpty() == False:
        [node, parent, cumulative_cost] = fringe.pop()        # node = [state, direction, cost]

        # if we already expand this node, skip this
        if (node[0] in closed) == True:
            continue
        
        # push state to the closed set, so that we don't have to expand children again
        closed.add(node[0])

        # record the parent pos of this pos
        parents[node[0]] = parent

        # check if pos is the goal
        if problem.isGoalState(node[0]):

            # Success! Find the goal! construct action path
            curr = node
            while curr[0] != problem.getStartState():   # loop from goal to the start
                parent = parents[curr[0]]               # get the parent of current state from dictionary
                actions.append(curr[1])                 # store the action to the list, which is one of 'North', 'West', 'East', or 'South'
                curr = parent

            actions.reverse()   # reverse the action list to start in the start state
            return actions

        # push the child of the node to the queue
        for successor in problem.getSuccessors(node[0]):
            # successor format: ((34, 15), 'South', 1)
            cost = cumulative_cost + successor[2]           # current cost + next cost
            fringe.push([successor, node, cost], cost)      # ([child, parent, cost], cost)

    print("Failed. Unable to find the goal!")
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    actions = []
    closed = set()                  # nodes that already passed by
    parents = dict()                # parent of a node
    fringe = util.PriorityQueue()   # priority queue
    fringe.push([[problem.getStartState(), None, 0], None, 0], 0)     # ([[pos, direction, cost], parent, cumulative_cost], cumulative_cost)

    while fringe.isEmpty() == False:
        [node, parent, cumulative_cost] = fringe.pop()        # node = [state, direction, cost]

        # if we already expand this node, skip this
        if (node[0] in closed) == True:
            continue
        
        # push state to the closed set, so that we don't have to expand children again
        closed.add(node[0])

        # record the parent pos of this pos
        parents[node[0]] = parent

        # check if pos is the goal
        if problem.isGoalState(node[0]):

            # Success! Find the goal! construct action path
            curr = node
            while curr[0] != problem.getStartState():   # loop from goal to the start
                parent = parents[curr[0]]               # get the parent of current state from dictionary
                actions.append(curr[1])                 # store the action to the list, which is one of 'North', 'West', 'East', or 'South'
                curr = parent

            actions.reverse()   # reverse the action list to start in the start state
            return actions

        # push the child of the node to the queue
        for successor in problem.getSuccessors(node[0]):
            # successor format: ((34, 15), 'South', 1)
            next_cumulative_cost = cumulative_cost + successor[2]
            cost = next_cumulative_cost + heuristic(successor[0], problem)                # cost = uniform cost + greedy cost
            fringe.push([successor, node, next_cumulative_cost], cost)                    # ([child, parent, next_cumulative_cost], cost)

    print("Failed. Unable to find the goal!")
    return []


def meetMiddle(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first in the priority set"""

    def heuristicFunc(position_1, position_2):
        xy1 = position_1
        xy2 = position_2
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

    def getOppositeAction(action):
        if action == 'North':
            return 'South'
        elif action == 'South':
            return 'North'
        elif action == 'East':
            return 'West'
        elif action == 'West':
            return 'East'
        else:
            print('Error. Invalid action ' + action + ' in getOppositeAction().')

    actions_F = []
    actions_B = []
    closed_F = set()  # nodes (pos) that already passed by forward
    closed_B = set()  # nodes (pos) that already passed by backward
    parents_F = dict()  # parent of a forward node
    parents_B = dict()  # parent of a backward node
    open_F = util.PriorityQueue()  # forward priority queue
    open_B = util.PriorityQueue()  # backward priority queue
    open_F.push([[problem.getStartState(), None, 0], None, 0, 0, 0], 0)
    open_B.push([[problem.goal, None, 0], None, 0, 0, 0], 0)
    utility = sys.maxsize
    epsilon = 1

    while (open_F.isEmpty() == False) and (open_B.isEmpty() == False):

        [node_F, parent_F, pr_F, f_F, g_F] = open_F.top()  # node = [state, direction, cost]
        [node_B, parent_B, pr_B, f_B, g_B] = open_B.top()  # node = [state, direction, cost]

        # determine expand from forward or backward
        cost = min(pr_F, pr_B)

        # get f_min_F, f_min_B, g_min_F, g_min_B
        f_min_F = sys.maxsize
        f_min_B = sys.maxsize
        g_min_F = sys.maxsize
        g_min_B = sys.maxsize

        for i in range(open_F.size()):
            f_min_F = min(f_min_F, open_F.getItem(i)[2][2])  # open_F.getItem(i)[2] = [node_F, pr_F, f_F, g_F]
            g_min_F = min(g_min_F, open_F.getItem(i)[2][3])

        for i in range(open_B.size()):
            f_min_B = min(f_min_B, open_B.getItem(i)[2][2])
            g_min_B = min(g_min_B, open_B.getItem(i)[2][3])

        if utility <= max(cost, f_min_F, f_min_B, g_min_F + g_min_B + epsilon):
            print("Success. Construct the path!")
            if type(problem) is searchAgents.PositionSearchProblem:
                problem.displayExpand(meet_node[0], success=True)
                print(meet_node[0])

            # ----------- construct forward path -----------
            # find meet_node in open_F
            [curr, parent, pr, f, g] = open_F.getItemWithPos(meet_node[0])

            # record the parent of this pos
            parents_F[curr[0]] = parent

            while curr[0] != problem.getStartState():  # loop from meet point to the start
                parent = parents_F[curr[0]]  # get the parent of current state from dictionary
                actions_F.append(
                    curr[1])  # store the action to the list, which is one of 'North', 'West', 'East', or 'South'
                curr = parent

            actions_F.reverse()  # reverse the action list to start in the start state

            # ----------- construct backward path -----------
            # find meet_node in open_B
            [curr, parent, pr, f, g] = open_B.getItemWithPos(meet_node[0])

            # record the parent of this pos
            parents_B[curr[0]] = parent

            while curr[0] != problem.goal:  # loop from meetPoint to the goal
                parent = parents_B[curr[0]]  # get the parent of current state from dictionary
                action = getOppositeAction(curr[1])  # store the action in opposite directions for backward
                actions_B.append(action)
                curr = parent

            # ----------- connect forward and backward path -----------
            actions = actions_F + actions_B

            return actions

        # ----------- expand in the forward direction -----------
        if cost == pr_F:
            open_F.pop()

            # for display purpose
            if type(problem) is searchAgents.PositionSearchProblem:
                problem.displayExpand(node_F[0], success=False)

            # move node_F from open to closed
            closed_F.add(node_F[0])

            # record the parent of this pos
            parents_F[node_F[0]] = parent_F

            # push the child of the node to the queue
            for successor in problem.getSuccessors(node_F[0]):
                # successor format: ((34, 15), 'South', 1)

                cost_n_c = successor[2]
                g_F_c = g_F + cost_n_c
                if heuristic==nullHeuristic:
                    h_F_c = 0
                else:
                    h_F_c = heuristicFunc(successor[0], problem.goal)
                f_F_c = g_F_c + h_F_c

                if ((open_F.exist(successor[0])) or (successor[0] in closed_F)) and (g_F_c <= (g_F + cost_n_c)):
                    continue

                if (open_F.exist(successor[0])) or (successor[0] in closed_F):
                    open_F.remove(successor)  # TODO : add remove() in priority queue function
                    closed_F.remove(successor)

                    # add c to open_F
                pr_c = max(f_F_c, 2 * g_F_c)
                open_F.push([successor, node_F, pr_c, f_F_c, g_F_c],
                            pr_c)  # ([child, parent, priority_queue_value, f_F_c, g_F_c], priority_queue_value)

                if open_B.exist(successor[0]):
                    node_in_open_B = open_B.getItemWithPos(
                        successor[0])  # node_in_open_B: [node, parent, priority_queue_value, f, g]
                    g_B_c = node_in_open_B[4]

                    # utility = min(utility, g_B_c + g_F_c)
                    if utility > g_F_c + g_B_c:
                        meet_node = successor
                        utility = g_F_c + g_B_c

        # ----------- expand in the backward direction -----------
        else:
            open_B.pop()

            # for display purpose
            if type(problem) is searchAgents.PositionSearchProblem:
                problem.displayExpand(node_B[0], success=False)

            # move node_B from open to closed
            closed_B.add(node_B[0])

            # record the parent of this pos
            parents_B[node_B[0]] = parent_B

            # push the child of the node to the queue
            for successor in problem.getSuccessors(node_B[0]):
                # successor format: ((34, 15), 'South', 1)

                cost_n_c = successor[2]
                g_B_c = g_B + cost_n_c
                if heuristic==nullHeuristic:
                    h_B_c = 0
                else:
                    h_B_c = heuristicFunc(successor[0], problem.getStartState())
                f_B_c = g_B_c + h_B_c

                if ((open_B.exist(successor[0])) or (successor[0] in closed_B)) and (g_B_c <= (g_B + cost_n_c)):
                    continue

                if (open_B.exist(successor[0])) or (successor[0] in closed_B):
                    open_B.remove(successor)  # TODO : add remove() in priority queue function
                    closed_B.remove(successor)

                    # add c to open_B
                pr_c = max(f_B_c, 2 * g_B_c)
                open_B.push([successor, node_B, pr_c, f_B_c, g_B_c],
                            pr_c)  # ([child, parent, priority_queue_value, f_B_c, g_B_c], priority_queue_value)

                if open_F.exist(successor[0]):
                    node_in_open_F = open_F.getItemWithPos(
                        successor[0])  # node_in_open_F: [node, parent, priority_queue_value, f, g]
                    g_F_c = node_in_open_F[4]

                    # utility = min(utility, g_B_c + g_F_c)
                    if utility > g_B_c + g_F_c:
                        meet_node = successor
                        utility = g_B_c + g_F_c

    print("Failed. Unable to find the path!")
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
mm = meetMiddle
