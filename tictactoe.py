"""
Tic Tac Toe Player
"""

from copy import deepcopy

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


def player(board: list):
    """
    Returns player who has the next turn on a board.
    """
    turn = X if sum(cell.count(EMPTY) for cell in board) % 2 == 1 else O
    return turn


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = [(i, j) for i in range(3)
             for j in range(3) if board[i][j] == EMPTY]
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise ValueError("Invalid move")

    curr_board = deepcopy(board)
    curr_board[i][j] = player(curr_board)
    return curr_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontal check
    Hx = any(True for row in board if row.count(X) == 3)
    Ho = any(True for row in board if row.count(O) == 3)
    # Vertical check
    Vx = any(all(board[i][j] == X for i in range(3)) for j in range(3))
    Vo = any(all(board[i][j] == O for i in range(3)) for j in range(3))
    # Diagonal check
    D1 = [(0, 0), (1, 1), (2, 2)]
    D2 = [(0, 2), (1, 1), (2, 0)]
    Dx = any(all(board[i][j] == X for i, j in D) for D in [D1, D2])
    Do = any(all(board[i][j] == O for i, j in D) for D in [D1, D2])

    if any((Hx, Vx, Dx)):
        return X
    elif any((Ho, Vo, Do)):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or not len(actions(board)):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        best = max_value(board, float('-inf'), float('inf'))
        return best['action']
    else:
        best = min_value(board, float('-inf'), float('inf'))
        return best['action']


def max_value(board, alpha, beta):
    if terminal(board):
        return {'val': utility(board), 'action': None}
    v = float('-inf')
    best_action = None
    for action in actions(board):
        min_val = min_value(result(board, action), alpha, beta)['val']
        if min_val > v:
            v = min_val
            best_action = action
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return {'val': v, 'action': best_action}


def min_value(board, alpha, beta):
    if terminal(board):
        return {'val': utility(board), 'action': None}
    v = float('inf')
    best_action = None
    for action in actions(board):
        max_val = max_value(result(board, action), alpha, beta)['val']
        if max_val < v:
            v = max_val
            best_action = action
        beta = min(beta, v)
        if beta <= alpha:
            break
    return {'val': v, 'action': best_action}


def review(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return {'val': utility(board), 'move': None}

    if player(board) == X:
        best = {'val': -float('inf'), 'move': None}
        for action in actions(board):
            val, move = review(result(board, action)).values()
            if val > best['val']:
                best['val'] = val
                best['move'] = action
                if best['val'] == 1:
                    return best
    else:
        best = {'val': float('inf'), 'move': None}
        for action in actions(board):
            val, move = review(result(board, action)).values()
            if val < best['val']:
                best['val'] = val
                best['move'] = action
                if best['val'] == -1:
                    return best
    return best
