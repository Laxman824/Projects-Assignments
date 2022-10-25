# search.py



"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    startpoint=problem.getStartState()
    stack_dfs = util.Stack()
    walked = []
    stack_dfs.push((startpoint,[],0))
    while not stack_dfs.isEmpty():
    	successor, action, cost = stack_dfs.pop()
    	if problem.isGoalState(successor):
    		return action
    	if successor not in walked:
    		walked.append(successor)
    		for a, b, c in problem.getSuccessors(successor):
    		    stack_dfs.push((a, action+[b], c))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    startpoint=problem.getStartState()
    queue_bfs = util.Queue()
    walked = []
    queue_bfs.push((startpoint,[],0))
    while not queue_bfs.isEmpty():
        successor, action, cost = queue_bfs.pop()
        if problem.isGoalState(successor):
            return action
        if successor not in walked:
            walked.append(successor)
            for a, b, c in problem.getSuccessors(successor):
                queue_bfs.push((a, action+[b], c))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    startpoint=problem.getStartState()
    ucs = util.PriorityQueue()
    dictionary = util.Counter()
    walked = []
    ucs.push((startpoint,[],0), dictionary[str(startpoint[0])])
    while not ucs.isEmpty():
        successor, action, cost = ucs.pop()
        if problem.isGoalState(successor):
            return action
        if successor not in walked:
            walked.append(successor)
            for a, b, c in problem.getSuccessors(successor):
                dictionary[str(a)] = problem.getCostOfActions(action+[b])
                ucs.push((a, action+[b], c), dictionary[str(a)])
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startpoint=problem.getStartState()
    astar = util.PriorityQueue()
    dictionary = util.Counter()
    walked = []
    dictionary[str(startpoint[0])]+=heuristic(startpoint,problem)
    astar.push((startpoint,[],0), dictionary[str(startpoint[0])])
    while not astar.isEmpty():
        successor, action, cost = astar.pop()
        if problem.isGoalState(successor):
            return action
        if successor not in walked:
            walked.append(successor)
            for a, b, c in problem.getSuccessors(successor):
                dictionary[str(a)] = problem.getCostOfActions(action+[b])+heuristic(a,problem)
                astar.push((a, action+[b], c), dictionary[str(a)])

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
