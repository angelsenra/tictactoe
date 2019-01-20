#! python3
import logging
import random
import time

import numpy as np

logger = logging.getLogger("ai")
logger.setLevel(logging.DEBUG)

_WINNING_ROWS = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
                 (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
                 (0, 4, 8), (2, 4, 6))             # Diagonal
WINNING_ROWS = np.array([[i in row for i in range(9)]
                         for row in _WINNING_ROWS], np.int8).T
ADD = np.eye(9, dtype=np.int8)  # 9x9 0s array with a diagonal of 1s
EMPTY = np.zeros(9, dtype=np.int8)

HUMAN = -1
AI = 1
TURN_HUMAN = (ADD * HUMAN, min)  # Minimum ganance for AI
TURN_AI = (ADD * AI, max)  # Maximum ganance for AI

RANDOM = 1
MINIMAX = 2


class cache_board:
    def __init__(self, func):
        self.cache = {}
        self.func = func

    def __call__(self, *arg, **kw):
        s = arg[0].tostring()
        try:
            return self.cache[(s, *arg[1:2])]
        except KeyError:
            r = self.func(*arg, **kw)
            self.cache[(s, *arg[1:2])] = r
            return r


@cache_board
def winner(board):
    product = np.dot(board, WINNING_ROWS)
    if 3 in product:
        return 1
    elif -3 in product:
        return -1
    return 0


@cache_board
def minimax(board, userTurn, depth):
    whoWon = winner(board)
    if whoWon:
        return (15 * whoWon - depth, None)
    elif all(board) or not depth:
        return (0, None)
    add, function = TURN_HUMAN if userTurn else TURN_AI
    return function((minimax(board + add[i], not userTurn, depth - 1)[0], i)
                    for i in range(9) if not board[i])


def preload_minimax():
    logger.info("Pre-loading minimax")
    initialTime = time.time() * 1000
    minimax(np.zeros(9, dtype=np.int8), False, 9)
    for i in TURN_HUMAN[0]:
        minimax(i, False, 9)
    logger.info(f"Took {time.time() * 1000 - initialTime} ms")


def move(board, userTurn, difficulty):
    initialTime = time.time() * 1000
    r = random.choice([i for i in range(9) if not board[i]])
    m = minimax(board, userTurn, 9)[1]

    if difficulty == RANDOM:
        logger.debug("RANDOM")
        output = r
    elif difficulty == MINIMAX:
        logger.debug(f"MINIMAX level 9")
        output = m
    else:
        logger.warn(f"Wrong AI difficulty: {difficulty}")
        output = r
    logger.info(f"Took {time.time() * 1000 - initialTime} ms")
    return output
