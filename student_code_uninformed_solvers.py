
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
        # check victory statement
        # set visited
        # create children if don't exist

        if self.currentState.state == self.victoryCondition:
            return True
        self.visited[self.currentState] = True
        if len(self.currentState.children) == 0:
            moves = self.gm.getMovables()
            for child in moves:
                if self.gm.isMovableLegal(child):
                    self.gm.makeMove(child)
                    self.currentState.children.append(GameState(self.gm.getGameState(), self.currentState.depth + 1, child))
                    self.gm.reverseMove(child)
        for child in self.currentState.children:
            child.parent = self.currentState
            try:
                if self.visited[child] == True:
                    pass
            except KeyError:
                self.gm.makeMove(child.requiredMovable)
                self.currentState = child
                return False
        if isinstance(self.currentState.parent, GameState):
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return self.solveOneStep()
        return True




class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = []

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
        if self.currentState.state == self.victoryCondition:
            return True
        curr = self.currentState
        self.visited[self.currentState] = True
        if len(self.currentState.children) == 0:
            moves = self.gm.getMovables()
            for child in moves:
                if self.gm.isMovableLegal(child):
                    self.gm.makeMove(child)
                    self.currentState = GameState(self.gm.getGameState(), self.currentState.depth + 1, child)
                    self.currentState.parent = curr
                    self.currentState.parent.children.append(self.currentState)
                    self.queue.append(self.currentState)
                    self.gm.reverseMove(child)
                    self.currentState = self.currentState.parent
        undo = []
        while isinstance(curr.parent, GameState):
            undo.append(curr.requiredMovable)
            curr = curr.parent
        for x in undo:
            self.gm.reverseMove(x)

        while self.queue:
            front = self.queue.pop(0)
            self.currentState = front
            try:
                self.visited[front]
            except KeyError:
                make = []
                undo = []
                while isinstance(front.parent, GameState):
                    make.insert(0, front.requiredMovable)
                    undo.append(front.requiredMovable)
                    front = front.parent

                for x in make:
                    self.gm.makeMove(x)

                return False
        return True



