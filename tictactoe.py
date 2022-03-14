"""
Tic Tac Toe Player
"""

from json.encoder import INFINITY
import math
from msilib.schema import Error
from queue import Empty
import copy
from sre_parse import State

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Initial values
    x=0
    o=0 

    # Return o if x has played an extra turn over o (x always starts)
    for i in board:
        for j in i:
            if j=='X' :
                x+=1
            elif j==O:
                o+=1
    if x-o==1:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Define set of possible actions
    actionSet = set()

    # Find empty locations and adds them to the set of possible actions
    for i in range(len(board)):
        for j in range(len(board)):
            if not board[i][j]:
                actionSet.add((i, j))
    return actionSet




def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Get current player + make copied board
    currentPlayer = player(board)
    tempBoard = copy.deepcopy(board)

    # Check if action is valid
    if(tempBoard[action[0]][action[1]] == EMPTY):
        # Make the action on board
        tempBoard[action[0]][action[1]] = currentPlayer
        return tempBoard
    else:
        raise Error




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Get last player to return later as the winner
    lastPlayer = X if player(board) == O else O

    # Check for a 3 in a row win
    for i in board:
        if i[0] == i[1] == i[2] == lastPlayer :
            return lastPlayer
    # Check for 3 in a column win
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == lastPlayer :
            return lastPlayer
    # Check for both diagonal wins
    if board[0][0] == board[1][1] == board[2][2] == lastPlayer :
        return lastPlayer
    if board[2][0] == board[1][1] == board[0][2] == lastPlayer :
        return lastPlayer
    else :
        return EMPTY


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if a player has already won
    if winner(board):
        return True
    # Check if the board has possible moves left, return True otherwise (Draw)
    for i in board:
        for j in i:
            if not j:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Gets the winner using winner() function
    winPlayer = winner(board)
    # Retruns specified output
    if winPlayer == X:
        return 1
    elif winPlayer == O:
        return -1
    else :
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Returns max or min utility action depending on the current player
    # x is the maximizer, o is the minimizer
    if player(board) == X:
        return maxVal(board)[1]
    else :
        return minVal(board)[1]
    
    
def maxVal(board):
    if terminal(board):
        return [utility(board), EMPTY]
    v= [float('-inf'), EMPTY]
    for action in actions(board):
        ut = minVal(result(board, action))[0]
        if ut > v[0]:
            v[0] = ut
            v[1] = action
    return v


def minVal(board):
    if terminal(board):
        return [utility(board), EMPTY]
    v= [float('inf'), EMPTY]
    for action in actions(board):
        ut = maxVal(result(board, action))[0]
        if ut < v[0]:
            v[0] = ut
            v[1] = action
    return v


