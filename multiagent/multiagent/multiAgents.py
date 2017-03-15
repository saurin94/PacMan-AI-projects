# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        #print "new Ghost States:" , newGhostStates
        "*** YOUR CODE HERE ***"

        FoodList = newFood.asList()

        foodMin = float("inf")
        ghostMin = float("inf")
        FoodListCount = len(FoodList)
        i = 0
        while i < FoodListCount :
            distancetoFood = util.manhattanDistance(newPos, FoodList[i])
            if distancetoFood < foodMin and  distancetoFood != 0:
                foodMin = distancetoFood
            i = i + 1

        ghostPositions = [ghostState.getPosition() for ghostState in newGhostStates]
        ghostPositionsLength = len(ghostPositions)

        j = 0
        while j < ghostPositionsLength :
            distancetoGhost = util.manhattanDistance(newPos , ghostPositions[j])
            if distancetoGhost < ghostMin :
                ghostMin = distancetoGhost
            j = j + 1

        if ghostMin <= 1:
            ghostMin = -(float("inf"))
        else:
            for ghostState in newGhostStates:
                if ghostState.scaredTimer>0 and ghostMin>1:
                    ghostMin = 1

        # ghostScore = 0
        # for ghostState in newGhostStates:
        #     if ghostState.scaredTimer > 0 and ghostMin <= 1:
        #         ghostScore = -1.0 / (ghostMin)
        #         ghostMin = -(float('inf'))
        #     elif ghostState.scaredTimer < ghostMin:
        #         ghostScore = 1.0 / ghostMin
        #     else:
        #         ghostScore = +1.0 / ghostMin

        FinalScore = (ghostMin/(100*foodMin)) + successorGameState.getScore()

        return FinalScore

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
        """
        "*** YOUR CODE HERE ***"
        # Pacman is always agent index 0 . Let pacmans turn be 0.
        turnPacman = 0

        def maxAgent(state, depth):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            ListOfActions = state.getLegalActions(turnPacman)
            v = -float("infinity")
            lenListOfActions = len(ListOfActions)
            lastAction = Directions.STOP
            i = 0
            while i != lenListOfActions:
                successor = state.generateSuccessor(turnPacman, ListOfActions[i])
                _new_v = minAgent(successor, depth, 1)
                if _new_v > v:
                    v = max(_new_v,v)
                    lastAction = ListOfActions[i]
                i = i+1
            if depth == 0:
                return lastAction
            else:
                return v


        def minAgent(state, depth, nextTurn):
            if state.isLose() or state.isWin():
                return self.evaluationFunction(state)
            PacmansNextTurn = nextTurn + 1
            if nextTurn == state.getNumAgents() - 1:
                PacmansNextTurn = turnPacman
            ListOfActions = state.getLegalActions(nextTurn)
            v = float("infinity")
            lenActions = len(ListOfActions)
            i= 0
            while i != lenActions:
                successor = state.generateSuccessor(nextTurn , ListOfActions[i])
                # if it is pacmans turn
                if PacmansNextTurn == turnPacman:
                    if depth == self.depth - 1:
                        _new_v = self.evaluationFunction(successor)
                    else:
                        _new_v = maxAgent(successor, depth + 1)
                else:
                    _new_v = minAgent(successor, depth, PacmansNextTurn)
                if _new_v < v:
                    v = min(_new_v,v)
                i = i+1
            return v

        return maxAgent(gameState, 0)






class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        turnPacman = 0

        def maxAgent(state, depth, alpha, beta):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            ListOfActions = state.getLegalActions(turnPacman)
            v = -float("infinity")
            lastAction = Directions.STOP
            lenListOfActions = len(ListOfActions)
            i = 0
            while i != lenListOfActions:
                successor = state.generateSuccessor(turnPacman, ListOfActions[i])
                new_v = minAgent(successor, depth, 1,alpha,beta)
                if new_v > v:
                    v = max(new_v,v)
                    lastAction = ListOfActions[i]
                alpha = max(alpha, v)
                if v > beta:
                    return v
                i = i + 1
            if depth == 0:
                return lastAction
            else:
                return v

        def minAgent(state, depth, nextTurn, alpha, beta):
            if state.isLose() or state.isWin():
                return state.getScore()
            PacmansNextTurn = nextTurn + 1
            if nextTurn == state.getNumAgents() - 1:
                PacmansNextTurn = turnPacman
            v = float("inf")
            ListOfActions = state.getLegalActions(nextTurn)
            lastAction = Directions.STOP
            lenListOfActions = len(ListOfActions)
            i = 0
            while i != lenListOfActions:
                successor = state.generateSuccessor(nextTurn, ListOfActions[i])
                if PacmansNextTurn == turnPacman:

                    if depth == self.depth - 1:
                        new_v = self.evaluationFunction(successor)
                    else:
                        new_v = maxAgent(successor, depth + 1, alpha, beta)

                else:
                    new_v = minAgent(successor, depth, PacmansNextTurn, alpha, beta)
                if new_v < v:
                    v = min(v,new_v)
                beta = min(beta, v)
                if v < alpha:
                    return v
                i = i+1
            return v

        return maxAgent(gameState, 0, float("-inf"), float("inf"))


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

        def maxAgent(gameState, depth):
            if depth == self.depth:
                return (self.evaluationFunction(gameState), None)

            ListOfActions = gameState.getLegalActions(0)
            v = -float("infinity")
            lastAction = None

            if len(ListOfActions) == 0:
                return (self.evaluationFunction(gameState), None)
            i = 0
            while i != len(ListOfActions):
                successor = gameState.generateSuccessor(0, ListOfActions[i])
                new_v = minAgent(successor, 1, depth)[0]
                if (new_v > v):
                    v, lastAction = max(new_v,v), ListOfActions[i]
                i = i + 1
            return (v, lastAction)

        def minAgent(gameState, turn, depth):

            lastAction = None
            ListOfActions = gameState.getLegalActions(turn)
            prob = 0

            if len(ListOfActions) == 0:
                return (self.evaluationFunction(gameState), None)
            i = 0
            while i != len(ListOfActions):
                successor = gameState.generateSuccessor(turn, ListOfActions[i])
                if (turn == gameState.getNumAgents() - 1):
                    new_v = maxAgent(successor, depth + 1)[0]
                else:
                    new_v = minAgent(successor, turn + 1, depth)[0]
                prob += new_v / len(ListOfActions)
                i = i+1
            return (prob, lastAction)

        return maxAgent(gameState, 0)[1]



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
     1. Calculated the minimum distance to food.
     2. Calculated the distance to ghost. The min distance to any ghost.
     3. If the ghost is very close , that is less than 2 places, increase the factor to a huge number
     4. Calculated the ghostScore if the ghost Scared time is greater than zero , given huge values to the score
     5. If scared time is not greater than zero , giving the ghostScore lesser values.
     6. This evaluates the pacman as per food Distance, ghost Distance, and ghost Scared Time.

    """
    "*** YOUR CODE HERE ***"
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    # print "new Ghost States:" , newGhostStates
    "*** YOUR CODE HERE ***"

    FoodList = newFood.asList()

    foodMin = float("inf")
    ghostMin = float("inf")
    FoodListCount = len(FoodList)
    i = 0
    while i < FoodListCount:
        distancetoFood = util.manhattanDistance(newPos, FoodList[i])
        if distancetoFood < foodMin and distancetoFood != 0:
            foodMin = distancetoFood
        i = i + 1

    ghostPositions = [ghostState.getPosition() for ghostState in newGhostStates]
    ghostPositionsLength = len(ghostPositions)

    j = 0
    while j < ghostPositionsLength:
        distancetoGhost = util.manhattanDistance(newPos, ghostPositions[j])
        if distancetoGhost < ghostMin:
            ghostMin = distancetoGhost
        j = j + 1

    if ghostMin < 2:
        ghostMin = -(float("inf"))
    ghostScore = 0
    for ghostState in newGhostStates:
        if ghostState.scaredTimer > 0 and ghostMin <= 1:
            ghostScore = -1.0/(ghostMin)
            ghostMin = -(float('inf'))
        elif ghostState.scaredTimer < ghostMin:
            ghostScore = 1.0/ghostMin
        else:
            ghostScore = +1.0/ghostMin


    FinalScore = 1/(foodMin) + 1/(10 + 0.5*len(FoodList)) + 1/(ghostMin) + ghostScore/0.5 + successorGameState.getScore()

    return FinalScore


# Abbreviation
better = betterEvaluationFunction

