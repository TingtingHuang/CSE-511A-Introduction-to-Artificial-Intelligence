# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import heapq
import searchAgents


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Stack(); #create an empty fringe using a LIFO queue
    root = (problem.getStartState(), [], 0); #make a (successor, action, stepCost) triple
    fringe.push(root); #Initialize the fringe using the start with cost 0
    visited = []; #create an empty set for visited nodes. 
    frontier = [] #create an empty set to store the positions in fringe
    while not fringe.isEmpty():
        state, direction, cost = fringe.pop(); #choose the deepest leaf node
        if problem.isGoalState(state):
            return direction #if the node contains a goal state then return the solution
        visited.append(state); #if not, add the node to visited list
        for node in fringe.list:
            frontier.append(node[0]) #Take out the positions stored in fringe
        for cstate, cdirection, ccost in problem.getSuccessors(state):

            if (cstate not in frontier) and (cstate not in visited):
                path = direction + [cdirection]; #store the directional path to each fringe node
                fringe.push((cstate, path, ccost)); 
                #expand the chosen node, and add the children nodes not in visited or fringe to fringe
    return [];
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Queue(); #create an empty fringe using a FIFO queue
    root = (problem.getStartState(), [], 0); #make a (successor, action, stepCost) triple
    fringe.push(root); #Initialize the fringe using the start with cost 0
    visited = []; #create an empty set for visited nodes. 
    frontier = [] #create an empty set to store the positions in fringe
    while not fringe.isEmpty():
        state, direction, cost = fringe.pop(); #choose the shallowest leaf node
        if problem.isGoalState(state):
            return direction #if the node contains a goal state then return the solution
        visited.append(state); #if not, add the node to visited list
        for node in fringe.list:
            frontier.append(node[0]) #Take out the positions stored in fringe
        for cstate, cdirection, ccost in problem.getSuccessors(state):
            if (cstate not in frontier) and (cstate not in visited):
                path = direction + [cdirection]; #store the directional path to each fringe node
                fringe.push((cstate, path, ccost)); 
                #expand the chosen node, and add the children nodes not in visited or fringe to fringe
    return [];
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    pathcost=0
    node = (pathcost, problem.getStartState(), [])
    frontier = [node]
    visited = []

    while len(frontier)>0:
        pathcost, state, direction =heapq.heappop(frontier)
#       print pathcost, state, direction
        if problem.isGoalState(state):
            return direction
        visited.append(state)
        for cstate,cdirection,ccost in problem.getSuccessors(state):            
            if (cstate not in frontier) and (cstate not in visited):
                child_node =((pathcost + ccost),cstate,direction+[cdirection])
#               print child_node
                heapq.heappush(frontier, child_node)            
            elif cstate in frontier:
                child_pathcost=pathcost+ccost
                for i in range(len(frontier)) :
                    if (frontier[i][1][1]==cstate) and ( child_pathcost < frontier[i][1][0]):
                        frontier[i][1][0] = child_pathcost

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    pathcost=0 
    heur=heuristic(problem.getStartState(),problem)
    node = (pathcost+heur, problem.getStartState(), [])
    frontier = [node]
    visited = []
    
    while len(frontier)<>0:
        cost, state, direction =heapq.heappop(frontier)
        heur = heuristic(state,problem)
        pathcost = cost - heur
        if problem.isGoalState(state):
            return direction
        visited.append(state)
        for cstate,cdirection,ccost in problem.getSuccessors(state):            
            if (cstate not in frontier) and (cstate not in visited):
                child_pathcost=pathcost + ccost
                child_heur=heuristic(cstate, problem)
                child_cost=child_pathcost+child_heur
                child_node =(child_cost, cstate,direction+[cdirection])
                heapq.heappush(frontier, child_node)            
            elif cstate in frontier:
                child_pathcost=pathcost+ccost
                for i in range(len(frontier)) :
                    if (frontier[i][1]==cstate) and ( child_cost < frontier[i][0]):
                        frontier[i][0] = child_cost

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
