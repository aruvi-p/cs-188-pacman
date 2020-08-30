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
import operator

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

        
        ghostdistance = []
        for ghoststate in newGhostStates:
            ghostdistance.append(manhattanDistance(newPos, ghoststate.getPosition()))
            
        if(len(ghostdistance) != 0):
            if min(ghostdistance) != 0:
                nearestghostdistance = 1/min(ghostdistance)
            else:
                nearestghostdistance = 1e4
            
        else:
            nearestghostdistance = 1e4
            
        foods = newFood.asList()
        
        fooddistance = []
        for food in foods:
            fooddistance.append(manhattanDistance(newPos, food))
            
        if len(fooddistance) != 0:
            nearestfood = min(fooddistance)
        else:
            nearestfood =0
            
        totalscore = -1*(nearestfood) - 5*(nearestghostdistance) - 100*len(foods)
            
        return totalscore
        
        
        
        
        #return successorGameState.getScore()

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
        
#        def minimax(agent, depth, gameState):
#            if gameState.isLose() or gameState.isWin() or depth == self.depth:  # return the utility in case the defined depth is reached or the game is won/lost.
#                return self.evaluationFunction(gameState)
#            if agent == 0:  # maximize for pacman
#                return max(minimax(1, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))
#            else:  # minize for ghosts
#                nextAgent = agent + 1  # calculate the next agent and increase depth accordingly.
#                if gameState.getNumAgents() == nextAgent:
#                    nextAgent = 0
#                if nextAgent == 0:
#                   depth += 1
#                return min(minimax(nextAgent, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))

    
        def minmax(agent, state, depth):

            if not (depth == (self.depth*state.getNumAgents()) or state.isLose() or state.isWin()):
                depth = depth + 1
                if agent == 0:
                    return max(minmax(1,state.generateSuccessor(agent,nextstate),depth) \
                               for nextstate in state.getLegalActions(agent))
                else:
                    if agent == state.getNumAgents() - 1:
                        n_agent = 0
                        
                    else:
                        n_agent = agent + 1
                    #print(n_agent, "is the agent now", state.getNumAgents(), "is the total agent" )    
                    return min(minmax(n_agent,state.generateSuccessor(agent,nextstate),depth)\
                               for nextstate in state.getLegalActions(agent))
            else:
                return self.evaluationFunction(state)
        action_value = {}
        for actions in gameState.getLegalActions(0):
            action_value[actions] = (minmax(1,gameState.generateSuccessor(0, actions),1))   
        final_action = max(action_value.items(), key=operator.itemgetter(1))[0]
        return final_action
                        
                    
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
#        def alphabeta(agent, depth,gameState,a,b):
#            
#            def max_func(agent, depth, gameState, a, b):  # maximizer function
#                v = float("-inf")
#                for newState in gameState.getLegalActions(agent):
#                    v = max(v, alphabeta(1, depth, gameState.generateSuccessor(agent, newState), a, b))
#                    if v > b:
#                        return v
#                    a = max(a, v)
#                return v
#
#            def min_func(agent, depth, gameState, a, b):  # minimizer function
#                v = float("inf")
#    
#                next_agent = agent + 1  # calculate the next agent and increase depth accordingly.
#                if gameState.getNumAgents() == next_agent:
#                    next_agent = 0
#    
#                for newState in gameState.getLegalActions(agent):
#                    v = min(v, alphabeta(next_agent, depth, gameState.generateSuccessor(agent, newState), a, b))
#                    if v < a:
#                        return v
#                    b = min(b, v)
#                return v
#
#            if not (depth == (self.depth*gameState.getNumAgents()) or gameState.isLose() or gameState.isWin()):
#                depth = depth + 1
#                if agent == 0:
#                    return max_func(agent, depth, gameState, a, b)
#                else:
#                    if agent == gameState.getNumAgents() - 1:
#                        n_agent = 0
#                        
#                    else:
#                        n_agent = agent + 1
#                    #print(n_agent, "is the agent now", state.getNumAgents(), "is the total agent" )    
#                    return min_func(n_agent, depth, gameState, a, b)
#            else:
#                return self.evaluationFunction(gameState)
#        action_value = {}
#        for actions in gameState.getLegalActions(0):
#            action_value[actions] = (alphabeta(1,1,gameState.generateSuccessor(0, actions),float("inf"),-float("inf")))   
#        final_action = max(action_value.items(), key=operator.itemgetter(1))[0]
#        return final_action
#                        
#                    
#        util.raiseNotDefined()


        
        
        def min_func(state, agent, depth, a, b):
            value = 1e20
            if (depth == ((self.depth)+1) or state.isLose() or state.isWin()):
                return self.evaluationFunction(state)

            for action in state.getLegalActions(agent):
                n_state = state.generateSuccessor(agent, action)
                
                if agent + 1 == state.getNumAgents():
                    
                    n_agent = 0
                    n_value = max_func(n_state, n_agent, depth, a, b)
                    
                else:
                    n_agent = agent + 1 
                    n_value = min_func(n_state, n_agent, depth, a, b)

                value = min(value, n_value)
                b = min(b, value)
                if value < a:
                    return value
                
            return value

        def max_func(state, agent, depth, a, b):
            value = -1*1e20
            if (depth == ((self.depth)) or state.isLose() or state.isWin()):
                return self.evaluationFunction(state)
            

            for action in state.getLegalActions(agent):
                n_value = min_func(state.generateSuccessor(0, action), 1, depth + 1, a, b)
                
                if n_value > value:
                    value = n_value
                    if depth == 0:
                        final_action = action
                if value > b:
                    return value
                a = max(a, value)

            if depth != 0:
                return value
            else:
                return final_action
            
        
        return max_func(gameState, 0,0, -1*1e20, 1e20)
    
        util.raiseNotDefined()

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
        def expectimax(state, agent, depth):
            
            if not (depth == (self.depth*state.getNumAgents()) or state.isLose() or state.isWin()):
                 
                depth = depth + 1
                if agent == 0:
                    return max(expectimax(state.generateSuccessor(agent,nextstate),1,depth)\
                               for nextstate in state.getLegalActions(agent))
                else:
                    if agent == state.getNumAgents() - 1:
                        n_agent = 0
                        
                    else:
                        n_agent = agent + 1
                    #print(n_agent, "is the agent now", state.getNumAgents(), "is the total agent" )    
                return sum((expectimax(state.generateSuccessor(agent,nextstate),n_agent,depth))\
                           for nextstate in state.getLegalActions(agent))/(len(state.getLegalActions(agent)))
            else:
                return self.evaluationFunction(state)

        action_value = {}
        for actions in gameState.getLegalActions(0):
            action_value[actions] = expectimax(gameState.generateSuccessor(0, actions),1,1)   
        final_action = max(action_value.items(), key=operator.itemgetter(1))[0]
        return final_action
                                                       
    

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    
    """
    "*** YOUR CODE HERE ***"

    position = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    ghoststates = currentGameState.getGhostStates()
    score = currentGameState.getScore()

    
    ghostdistance = []
    for ghoststate in ghoststates:
        ghostdistance.append(manhattanDistance(position, ghoststate.getPosition()))
        
    if(len(ghostdistance) != 0):
        if min(ghostdistance) != 0:
            nearestghostdistance = 1/min(ghostdistance)
        else:
            nearestghostdistance = 1e4
        
    else:
        nearestghostdistance = 1e4
        
    
    fooddistance = []
    for food in foods:
        fooddistance.append(manhattanDistance(position, food))
        
    if len(fooddistance) != 0:
        nearestfood = min(fooddistance)
    else:
        nearestfood =0
        
    totalscore = -2*(nearestfood) - 5*(nearestghostdistance) - 100*len(foods) + 10*score
    return totalscore

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
