# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
import itertools

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


    "*** YOUR CODE HERE ***"
    current_food_list = list(currentGameState.getFood().asList())
    food_list = list(newFood.asList())
    wall_list = list(currentGameState.getWalls().asList())
    score = successorGameState.getScore()
    x_newPos = newPos[0]
    y_newPos = newPos[1]
    neighbors = [((x_newPos-1),y_newPos),((x_newPos+1),y_newPos),(x_newPos,(y_newPos-1)),(x_newPos,(y_newPos+1))]
    food_distance = []
    if len(food_list)<>0: 
      for food in food_list:
        food_distance.append(util.manhattanDistance(newPos, food))
      min_food_distance = min(food_distance)
      if action <> 'Stop':
        score += (30-min_food_distance)*10/30
      else:
        score -= 10
      if newPos in current_food_list:
        score +=5
  
    for neighbor in neighbors:
      if neighbor in current_food_list:
        score +=1 
    for ghost_index in range(len(newGhostStates)):
      if newScaredTimes[ghost_index]>5 and util.manhattanDistance(newPos, newGhostStates[ghost_index].getPosition())<=20:
        dis=util.manhattanDistance(newPos, newGhostStates[ghost_index].getPosition())
        score +=(30-dis)*200/30
      elif newScaredTimes[ghost_index]<=5 and util.manhattanDistance(newPos, newGhostStates[ghost_index].getPosition())<=2:
        dis=util.manhattanDistance(newPos, newGhostStates[ghost_index].getPosition())
        score -=(30-dis)*200/30   
    
    return score

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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    legalActions = gameState.getLegalActions(0)
    legalActions.remove('Stop')
    
    besctaction = Directions.STOP
    score = float("-inf")
    for action in legalActions:
      child = gameState.generateSuccessor(0, action)
      newscore = max(score, minimax_value(self, child, self.depth, 1))
      if newscore > score:
        bestaction = action
      score = newscore
    
    return bestaction
  
def minimax_value(self, gameState, depth, agentIndex):
    ghostnumber = gameState.getNumAgents()-1

    if depth == 0 or gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)
    if agentIndex == 0:
      legalActions_pacman = gameState.getLegalActions(0)
      
      bestvalue = float("-inf")
      
      for action in legalActions_pacman:

        pacman_child = gameState.generatePacmanSuccessor(action)
        newscore = minimax_value(self, pacman_child, depth-1, 1)
        
        bestvalue = max(bestvalue, newscore)

      return bestvalue
      
    else:
      legalActions_ghost = gameState.getLegalActions(agentIndex)
      bestvalue = float("inf")
      if agentIndex == ghostnumber:
        
        for action in legalActions_ghost:
  
          ghost_child = gameState.generateSuccessor(agentIndex, action)
          bestvalue = min(bestvalue, minimax_value(self, ghost_child, depth-1, 0))
  
      else:
        
        for action in legalActions_ghost:
   
          ghost_child = gameState.generateSuccessor(agentIndex, action)
          bestvalue = min(bestvalue, minimax_value(self, ghost_child, depth, agentIndex+1))
   
      return bestvalue
      
   

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    legalActions = gameState.getLegalActions(0)
    legalActions.remove('Stop')
    alpha = float("-inf")
    beta = float("inf")
    
    besctaction = Directions.STOP
    score = float("-inf")
    for action in legalActions:
      child = gameState.generateSuccessor(0, action)
      newscore = max(score, alphabeta_value(self, child, self.depth, alpha, beta, 1))
      if newscore > score:
        bestaction = action
      score = newscore
    
    return bestaction
def alphabeta_value(self, gameState, depth, alpha, beta, agentIndex):
    ghostnumber = gameState.getNumAgents()-1

    if depth == 0 or gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)
    if agentIndex == 0:
      legalActions_pacman = gameState.getLegalActions(0)
      
      bestvalue = float("-inf")
      
      for action in legalActions_pacman:

        pacman_child = gameState.generatePacmanSuccessor(action)
        newscore = alphabeta_value(self, pacman_child, depth-1, alpha, beta, 1)
        
        bestvalue = max(bestvalue, newscore)
        alpha = max(alpha, bestvalue)
        if beta <= alpha:
          break

      return bestvalue
      
    else:
      legalActions_ghost = gameState.getLegalActions(agentIndex)
      bestvalue = float("inf")
      if agentIndex == ghostnumber:
        
        for action in legalActions_ghost:

          ghost_child = gameState.generateSuccessor(agentIndex, action)
          bestvalue = min(bestvalue, alphabeta_value(self, ghost_child, depth-1, alpha, beta, 0))
          beta = min(beta, bestvalue)
          if beta <= alpha:
            break
 
      else:
        
        for action in legalActions_ghost:
  
          ghost_child = gameState.generateSuccessor(agentIndex, action)
          bestvalue = min(bestvalue, alphabeta_value(self, ghost_child, depth, alpha, beta, agentIndex+1))

          beta = min(beta, bestvalue)
          if beta <= alpha:
            break
      return bestvalue

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
    legalActions = gameState.getLegalActions(0)
    legalActions.remove('Stop')
    
    besctaction = Directions.STOP
    score = float("-inf")
    for action in legalActions:
      child = gameState.generateSuccessor(0, action)
      newscore = max(score, expectmax_value(self, child, self.depth, 1))
      if newscore > score:
        bestaction = action
      score = newscore
    
    return bestaction
  
def expectmax_value(self, gameState, depth, agentIndex):
    ghostnumber = gameState.getNumAgents()-1

    if depth == 0 or gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)
    if agentIndex == 0:
      legalActions_pacman = gameState.getLegalActions(0)
      
      bestvalue = float("-inf")
      
      for action in legalActions_pacman:
 #       print "pacman act:", action
        pacman_child = gameState.generatePacmanSuccessor(action)
        newscore = expectmax_value(self, pacman_child, depth-1, 1)
        
        bestvalue = max(bestvalue, newscore)

      return bestvalue
      
    else:
      legalActions_ghost = gameState.getLegalActions(agentIndex)
      bestvalue = 0
      if agentIndex == ghostnumber:
        
        for action in legalActions_ghost:
   
          ghost_child = gameState.generateSuccessor(agentIndex, action)
          bestvalue += expectmax_value(self, ghost_child, depth-1, 0)
   
      else:
        
        for action in legalActions_ghost:
    
          ghost_child = gameState.generateSuccessor(agentIndex, action)
          bestvalue = expectmax_value(self, ghost_child, depth, agentIndex+1)
   
      return bestvalue/len(legalActions_ghost)

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    The total score can be divided into four parts:
    1. score1 is the original score of the current game state.
    2. We assign higher score if pacman is close to its closest food. Then,
       score2 is the sum of the 10/(minimum food distance) + the number of 
       remaining food
    3. We encourage the pacman to eat the power capsule if it is close to it. 
      Then, score3 is 100 is the disance to power copsule is no larger than 3
    4. If the ghosts are not scared, score4 will decrease by 1000/(gdist+1) when
      the ghost is closer than 2 manhattanDistance. If the ghosts are scared, then
      chasing the ghosts is encouraged. 
  """
  "*** YOUR CODE HERE ***"
  pos = currentGameState.getPacmanPosition()
  score1 = currentGameState.getScore()
  

  Food = currentGameState.getFood()
  foodlist = list(Food.asList())
  dist = []
  score2 = 0
  if len(foodlist) != 0:
    for food in foodlist:
      dist.append(manhattanDistance(pos, food))
    mindist = min(dist)
    score2 = 10/mindist + len(foodlist)

  score3 = 0
  for capsule in currentGameState.getCapsules():
    if manhattanDistance(pos, capsule) <= 3:
      score3 = 100

  score4 = 0
  GhostStates = currentGameState.getGhostStates()
  
  for ghostState in GhostStates:
    ScaredTimes = ghostState.scaredTimer

    gdist = manhattanDistance(pos, ghostState.getPosition())
    if ScaredTimes <= 1 and gdist <= 2:
      score4 -= 1000/(gdist+1)
    elif ScaredTimes > 2:
      if gdist <= 20:
        score4 += 500/(gdist+1) 

  return 1.5 * score1 + score2 + score3 + 3 * score4




# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

