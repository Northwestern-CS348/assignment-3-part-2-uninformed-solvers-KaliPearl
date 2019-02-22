
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        # get current . check visited . find moveables and put into children, if hasn't been visited
        # check children for next unvisited, return false and set current to child

        current = self.currentState
        if current.state == self.victoryCondition:
            return True
        depth = current.depth
        self.visited[current] = True
        children = current.children
        if len(children) == 0:
            moves = self.gm.getMovables()
            if moves:
                for x in moves:
                    self.gm.makeMove(x)
                    self.currentState.children.append(GameState(self.gm.getGameState(), depth + 1, current.state)) # current.state isn't a movable RIP
                    self.gm.reverseMove(x) # either makemove or reverse move doesn't work properly as it doesn't remove the old movable statements
            if not moves:
                self.gm.reverseMove(current.state) # this isnt a movable obkect
                # self.currentState =
                return False
        if current.nextChildToVisit == -1:
            self.gm.reverseMove(current.requiredMovable)
            self.gm.currentState = self.currentState.parent

        if current.nextChildToVisit != -1:
            nextnode = current.nextChildToVisit
            self.currentState.nextChildToVisit += 1

            if current.nextChildToVisit >= len(children):
                current.nextChildToVisit = -1
            self.currentState = current.children[nextnode]
            self.currentState.parent = current
            return False




class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
