# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.QValues = util.Counter() # A Counter is a dict with default 0

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        if (state, action) not in self.QValues:
            self.QValues[(state, action)] = 0 # If state has never been seen before, initialize its Q value to 0.0
        
        return self.QValues[(state, action)] # Return Q value of state-action


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        actions = self.getLegalActions(state)

        max_val = float('-inf')

        if len(actions) == 0: # If there are no legal actions, return 0.0
            return 0.0
        else: # Iterate over all actions for the given state and return the max Q value 
            for a in actions:
                if self.getQValue(state, a) >= max_val:
                    max_val = self.getQValue(state, a)

        return max_val

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        actions = self.getLegalActions(state)
        max_val = float('-inf')
        best_action = None

        if len(actions) == 0: # If there are no legal actions, return None
            return None
        else: # Iterate over all actions gor the given state and return the action corresponding to the state with max Q value
            for a in actions:
                if self.getQValue(state, a) == max_val:
                    best_action = random.choice((best_action, a))
                elif self.getQValue(state, a) > max_val:
                    max_val = self.getQValue(state, a)
                    best_action = a
        return best_action

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        if len(legalActions) == 0:
            return None
        else:
            prob = self.epsilon
            if util.flipCoin(prob):
                action = random.choice(legalActions)
            else:
                # action = self.computeActionFromQValues(state)
                # Using getPolicy function
                action = self.getPolicy(state)

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # Q(s, a) = (1-alpha)*Q(s, a) + (alpha)*(Reward + discount*Q_max(s', a'))
        curr_QValue = self.getQValue(state, action) # Q(s, a)
        # max_next_QValue = self.computeValueFromQValues(nextState) # Max Q(s', a')
        # Using getValue function
        max_next_QValue = self.getValue(nextState) # Max Q(s', a')

        curr_QValue = (1-self.alpha)*curr_QValue + (self.alpha*(reward + (self.discount*max_next_QValue))) # Updating Q(s, a)

        self.QValues[(state, action)] = curr_QValue # Updating Q value of given state at given action

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        Q_Val = 0
        featureVector = self.featExtractor.getFeatures(state, action)

        for f in featureVector: # Q(s, a) = summation of feature_i(s, a)*weight_i
            Q_Val += featureVector[f]*self.weights[f]

        return Q_Val

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        featureVector = self.featExtractor.getFeatures(state, action)

        curr_QValue = self.getQValue(state, action) # Q(s, a)

        max_next_QValue = self.getValue(nextState) # Q_max(s', a')

        for f in featureVector: # weight_i = weight_i + alpha*difference*feature_i(s, a) where difference is (reward + discount*Q_max(s', a')) - Q(s, a)
            difference = (reward + (self.discount*max_next_QValue) - curr_QValue) 
            self.weights[f] += self.alpha*difference*featureVector[f]

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
