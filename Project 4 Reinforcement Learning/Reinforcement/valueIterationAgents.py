# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        itr  = self.iterations

        for i in range(itr):
            # updating self.values collectively after the iteration
            temp_values = self.values.copy()

            states = self.mdp.getStates()
            for s in states:
                if self.mdp.isTerminal(s) == False:
                    actions = self.mdp.getPossibleActions(s)
                    max_val = float('-inf')
                    for a in actions:
                        # trans = self.mdp.getTransitionStatesAndProbs(s, a)
                        # res = 0
                        # for t in trans:
                        #     res += t[1]*(self.mdp.getReward(s, a, t[0]) + (self.discount*temp_values[t[1]]))

                        # Replacing Q value calculation with getQValue function
                        res = self.getQValue(s, a)
                        
                        if res > max_val:
                            max_val = res
                    temp_values[s] = max_val
            self.values = temp_values
        return

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        trans = self.mdp.getTransitionStatesAndProbs(state, action)
        res = 0
        for t in trans:

            # get transition state s'

            # get transition probability to state s'

            # Q_val is summation of T(s, a, s')*[R(s, a, s') + discount*V(s')]           

            # res += t[1]*(self.mdp.getReward(state, action, t[0]) + (self.discount*self.values[t[0]]))

            # replacing self.values() function with another pre-built function self.getValues(self, state)
            res += t[1]*(self.mdp.getReward(state, action, t[0]) + (self.discount*self.getValue(t[0])))

        return res

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # if agent is at terminal state, None action should be returned
        if self.mdp.isTerminal(state):
            return None

        # getting all possible actions at the state
        actions = self.mdp.getPossibleActions(state)

        # if no legal actions are present, None action should be returned
        if len(actions) == 0:
            return None

        max_val = float('-inf')
        res_action = None

        for a in actions:
            # Using computeQValueFromValues(state, action) function to find value corresponding to each action
            val = self.computeQValueFromValues(state, a)

            # Resultant action and Max value will only be replaced if val from current action is greater/equal to max value or there is no action and max value is 0
            # if val > max_val:
            if (val >= max_val) or (a == None):
                
                # replace resultant action and value with action returning maximum value
                res_action = a
                max_val = val

        return res_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        # Get state list before iteration
        states = self.mdp.getStates()

        itr  = self.iterations

        for i in range(itr):
            # Get single state from state list in each iteration
            state_update = states[i%len(states)]
            
            if self.mdp.isTerminal(state_update) == False:
                actions = self.mdp.getPossibleActions(state_update)
                max_val = float('-inf')
                for a in actions:
                    res = self.getQValue(state_update, a)
                    if res > max_val:
                        max_val = res
                self.values[state_update] = max_val
        return


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

