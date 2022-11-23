# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print("successorGameState: ")
        # print(successorGameState)
        # print("newPos: ")
        # print(newPos)
        # print("newFood: ")
        # print(newFood)
        # print("newGhostStates: ")
        # print(newGhostStates)
        # print("newScaredTimes: ")
        # print(newScaredTimes)
        
        # print(newFood.asList())
        # minimum food distance would be a good incentive for the pacman
        minFoodDist=float('inf')
        for i in newFood.asList():
            minFoodDist = min(minFoodDist, util.manhattanDistance(i, newPos))

        # ghosts distance can also be considered
        # minGhostDist = float('inf')
        ghostProximityPenalty = 0
        minGhostDist = 1
        for i in successorGameState.getGhostPositions():
            minGhostDist = min(minGhostDist, util.manhattanDistance(i, newPos))
            if minGhostDist<1:
                minGhostDist=1
                ghostProximityPenalty=1
        return successorGameState.getScore()+(1/minFoodDist)-ghostProximityPenalty -(1/minGhostDist); # Agent will go towards food but gets penalised if gets too close to ghosts
        # return successorGameState.getScore()+(1/minFoodDist);

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        
        return self.helperMinimax(gameState, 0, 0)[0] # return agent action

    def helperMinimax(self, gameState, agentIndex, agentDepth):

        # agent 0 is pacman (max agent), other agents are ghosts(min agent)
        # once all agents have completed a turn, the cycle should reset
        if agentIndex>=gameState.getNumAgents(): 
            agentIndex = 0
            agentDepth = agentDepth+1

        # game tree should be stopped after expansion till custom depth
        if agentDepth==self.depth:
            return None, self.evaluationFunction(gameState)

        # return if game is over (win/lose)
        if gameState.isWin() or gameState.isLose():
            return None, self.evaluationFunction(gameState)

        # agentResult = [None, None]

        if agentIndex==0: # agent 0 is pacman which would maximise the utility
            return self.helperMax(gameState, agentIndex, agentDepth)
            # for i in gameState.getLegalActions(agentIndex):
            #     newState = gameState.generateSuccessor(agentIndex, i)
            #     newAction, newVal = self.helperMinimax(newState, agentIndex+1, agentDepth)
            #     if agentResult[1]==None or agentResult[1]<newVal:
            #         agentResult=[i, newVal]
        else: # agent >0 are ghosts which would minimise the utility
            return self.helperMin(gameState, agentIndex, agentDepth)
            # for i in gameState.getLegalActions(agentIndex):
                # newState = gameState.generateSuccessor(agentIndex, i)
                # newAction, newVal = self.helperMinimax(newState, agentIndex+1, agentDepth)
                # if agentResult[1]==None or agentResult[1]>newVal:
                #     agentResult=[i, newVal]

        # if agentResult[1]==None:
        #     agentResult=[None, scoreEvaluationFunction(gameState)]
        return agentResult

    #max agent
    def helperMax(self, gameState, agentIndex, agentDepth):
        agentResult = [None, float('-inf')]
        for i in gameState.getLegalActions(agentIndex):
            newState = gameState.generateSuccessor(agentIndex, i)
            newAction, newVal = self.helperMinimax(newState, agentIndex+1, agentDepth)
            if agentResult[1]<newVal:
                agentResult=[i, newVal]
        return agentResult

    #min agent
    def helperMin(self, gameState, agentIndex, agentDepth):
        agentResult = [None, float('inf')]
        for i in gameState.getLegalActions(agentIndex):
            newState = gameState.generateSuccessor(agentIndex, i)
            newAction, newVal = self.helperMinimax(newState, agentIndex+1, agentDepth)
            if agentResult[1]>newVal:
                agentResult=[i, newVal]
        return agentResult

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        return self.helperAlphaBeta(gameState, 0, 0, float('-inf'), float('inf'))[0] # passing alpha beta values

    def helperAlphaBeta(self, gameState, agentIndex, agentDepth, alphaVal, betaVal):

        if agentIndex>=gameState.getNumAgents(): 
            agentIndex = 0
            agentDepth = agentDepth+1

        if agentDepth==self.depth:
            return None, self.evaluationFunction(gameState)

        if gameState.isWin() or gameState.isLose():
            return None, self.evaluationFunction(gameState)

        if agentIndex==0: 
            return self.helperMax(gameState, agentIndex, agentDepth, alphaVal, betaVal)
        else:
            return self.helperMin(gameState, agentIndex, agentDepth, alphaVal, betaVal)

        return agentResult

    def helperMax(self, gameState, agentIndex, agentDepth, alphaVal, betaVal):
        agentResult = [None, float('-inf')]
        for i in gameState.getLegalActions(agentIndex):
            newState = gameState.generateSuccessor(agentIndex, i)
            newAction, newVal = self.helperAlphaBeta(newState, agentIndex+1, agentDepth, alphaVal, betaVal)
            if agentResult[1]<newVal:
                agentResult=[i, newVal]
            if agentResult[1]>betaVal:
                return agentResult
            alphaVal = max(alphaVal, agentResult[1]) #updating alpha if higher value is found in max node
        return agentResult

    def helperMin(self, gameState, agentIndex, agentDepth, alphaVal, betaVal):
        agentResult = [None, float('inf')]
        for i in gameState.getLegalActions(agentIndex):
            newState = gameState.generateSuccessor(agentIndex, i)
            newAction, newVal = self.helperAlphaBeta(newState, agentIndex+1, agentDepth, alphaVal, betaVal)
            if agentResult[1]>newVal:
                agentResult=[i, newVal]
            if agentResult[1]<alphaVal:
                return agentResult
            betaVal = min(betaVal, agentResult[1]) #updating beta if lower value is found in min node
        return agentResult

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        return self.helperExpectimax(gameState, 0, 0)[0]

    def helperExpectimax(self, gameState, agentIndex, agentDepth):

        if agentIndex>=gameState.getNumAgents(): 
            agentIndex = 0
            agentDepth = agentDepth+1

        if agentDepth==self.depth:
            return None, self.evaluationFunction(gameState)

        if gameState.isWin() or gameState.isLose():
            return None, self.evaluationFunction(gameState)

        if agentIndex==0: 
            return self.helperMax(gameState, agentIndex, agentDepth)
        else:
            return self.helperMinChance(gameState, agentIndex, agentDepth)

        return agentResult

    def helperMax(self, gameState, agentIndex, agentDepth):
        agentResult = [None, float('-inf')]
        for i in gameState.getLegalActions(agentIndex):
            newState = gameState.generateSuccessor(agentIndex, i)
            newAction, newVal = self.helperExpectimax(newState, agentIndex+1, agentDepth)
            if agentResult[1]<newVal:
                agentResult=[i, newVal]
        return agentResult

    def helperMinChance(self, gameState, agentIndex, agentDepth):
        agentResult = [None, 0]
        stateChance = 1.0/len(gameState.getLegalActions(agentIndex))
        for i in gameState.getLegalActions(agentIndex):
            newState = gameState.generateSuccessor(agentIndex, i)
            newAction, newVal = self.helperExpectimax(newState, agentIndex+1, agentDepth)
            agentResult[1]=agentResult[1]+(newVal*stateChance)
        agentResult[0]=random.choice(gameState.getLegalActions(agentIndex))
        return agentResult
