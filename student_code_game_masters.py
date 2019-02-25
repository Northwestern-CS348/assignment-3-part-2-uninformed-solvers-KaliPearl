from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peglist = ["peg1", "peg2", "peg3"]
        ret = ()
        for peg in peglist:
            bindings = self.kb.kb_ask(parse_input("fact: (on ?X " + peg + ")"))
            disklist = []
            t = ()
            if bindings:
                for x in bindings:
                    disklist.append(int(x.bindings[0].constant.element[-1]))
                disklist.sort()
                for x in disklist:
                    t += (x,)
            ret += (t,)
        return ret

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if movable_statement.predicate != "movable":
            return
        disk = "disk" + str(movable_statement.terms[0])[-1]
        startpeg = "peg" + str(movable_statement.terms[1])[-1]
        endpeg = "peg" + str(movable_statement.terms[2])[-1]

        self.kb.kb_retract(parse_input('fact: (on ' + disk + ' ' + startpeg + ')'))
        self.kb.kb_retract(parse_input('fact: (top ' + disk + ' ' + startpeg + ')'))

        on = self.kb.kb_ask(parse_input('fact: (on ' + '?X ' + startpeg + ')'))
        if not on: self.kb.kb_assert(parse_input('fact: (empty ' + startpeg + ')'))
        else:
            lst = []
            for x in on:
                lst += x.bindings[0].constant.element[-1]
            lst.sort(key=lambda x: int(x))
            self.kb.kb_assert(parse_input('fact: (top ' + "disk" + lst[0] + ' ' + startpeg + ')'))
        empty = self.kb.kb_ask(parse_input('fact: (empty ?X)'))
        if empty:
            for x in empty:
                if x.bindings[0].constant.element == endpeg:
                    self.kb.kb_retract(parse_input('fact: (empty ' + endpeg + ')'))
                    break
        top = self.kb.kb_ask(parse_input('fact: (top ?X ' + endpeg + ')'))
        if top:
            for x in top:
                self.kb.kb_retract(parse_input('fact: (top ' + "disk" + x.bindings[0].constant.element[-1] + ' ' + endpeg + ')'))
        self.kb.kb_assert(parse_input('fact: (on ' + disk + ' ' + endpeg + ')'))
        self.kb.kb_assert(parse_input('fact: (top ' + disk + ' ' + endpeg + ')'))

        """
        retract on (recur on above)
        check to see whether we need to retract empty/ make empty
        """

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        rowlist = ['pos1', 'pos2', 'pos3']
        ret = ()
        for row in rowlist:
            t = ()
            for xpos in rowlist:
                bindings = self.kb.kb_ask(parse_input("fact: (posn ?tile " + xpos + " " + row + ")"))
                if bindings:
                    for x in bindings:
                        content = (x.bindings[0].constant.element[-1])
                        if content == 'y':
                            t+=(-1,)
                        else:
                            t += (int(content),)
            ret += (t,)
        return ret

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if movable_statement.predicate != "movable":
            return
        tile = str(movable_statement.terms[0])
        startx = str(movable_statement.terms[1])
        starty = str(movable_statement.terms[2])
        endx = str(movable_statement.terms[3])
        endy = str(movable_statement.terms[4])

        currtile = self.kb.kb_ask(parse_input('fact: (posn ?tile ' + endx + ' ' + endy + ')'))
        endtile = currtile[0].bindings[0].constant.element
        self.kb.kb_retract(parse_input('fact: (posn ' + endtile + ' ' + endx + ' ' + endy + ')'))
        self.kb.kb_retract(parse_input('fact: (posn ' + tile + ' ' + startx + ' ' + starty + ')'))
        self.kb.kb_assert(parse_input('fact: (posn ' + endtile + ' ' + startx + ' ' + starty + ')'))
        self.kb.kb_assert(parse_input('fact: (posn ' + tile + ' ' + endx + ' ' + endy + ')'))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
