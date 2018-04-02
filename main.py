#! python3
from logging import (
    getLogger,
    DEBUG)
import tkinter as tk
from tkinter import messagebox
from json import load

logger = getLogger("TicTacToe")
logger.setLevel(DEBUG)

V0 = " "
P1 = "X"
P2 = "O"
BUTTON_STYLE = {"bg": "#F0F0F0", "activebackground": "#F0F0F0", "bd": 7,
                "relief": "ridge", "overrelief": "groove", "text": V0}
CLICKED_STYLE = {"fg": "#FFF", "activeforeground": "#000",
                 "overrelief": "ridge"}
WINNING_ROWS = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6))


def winner(board):
    for row in WINNING_ROWS:
        first = board[row[0]]
        if not first:
            continue
        if first == board[row[1]] == board[row[2]]:
            return first
    return 0


def minimax(board, userTurn, depth):
    whoWon = winner(board)
    if whoWon == 2:
        return (15 - depth, None)
    elif whoWon == 1:
        return (-15 - depth, None)
    elif 0 not in board or depth < 1:
        return (0, None)
    values = []
    number, function = (1, min) if userTurn else (2, max)
    for a in range(9):
        if board[a]:
            continue
        testBoard = board[:]
        testBoard[a] = number
        values.append((minimax(testBoard, not userTurn, depth - 1)[0], a))
    return function(values)


class App(tk.Frame):
    def __init__(self, master, userStarts, difficulty, fontSize):
        tk.Frame.__init__(self, master)
        self.userStarts = userStarts  # If False the loser will start
        self.userTurn = self.userStarts
        self.difficulty = difficulty
        self.font = ("Arial", fontSize, "bold")
        self.buttons = []
        for a in range(9):
            button = tk.Button(command=self.press(a), font=self.font)
            button.place(relx=a % 3 / 3, rely=a // 3 / 3, relwidth=1 / 3,
                         relheight=1 / 3, anchor="nw")
            self.buttons.append(button)
        self.new()

    def new(self):
        if self.userStarts:
            self.userTurn = True
        self.board = [0] * 9
        for button in self.buttons:
            button.config(**BUTTON_STYLE)
        self.after_press()

    def ai_move(self):
        if not self.board[4]:
            button = 4
        else:
            button = minimax(self.board, False, self.difficulty)[1]
        if button is None or self.board[button]:
            logger.error("AI could not move.")
            return
        kw = {"text": P2, "bg": "#00F", "activebackground": "#00F"}
        self.buttons[button].config(**CLICKED_STYLE, **kw)
        self.board[button] = 2
        self.userTurn = True
        self.after_press()

    def press(self, button):
        def wrapper():
            if not self.userTurn:
                logger.error("It is not your turn yet.")
                return
            if self.board[button]:
                logger.error("Could not choose that button.")
                return
            kw = {"text": P1, "bg": "#F00", "activebackground": "#F00"}
            self.buttons[button].config(**CLICKED_STYLE, **kw)
            self.board[button] = 1
            self.userTurn = False
            self.after_press()
        return wrapper

    def after_press(self):
        if winner(self.board) or 0 not in self.board:
            if messagebox.askyesno("Replay", "Play Again?"):
                self.new()
        if not self.userTurn:
            self.ai_move()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.config(bg="white")
    root.iconbitmap(default="icon.ico")
    root.geometry("300x300+0+0")
    root.aspect(1, 1, 1, 1)  # Not working or not supported by my PC (?)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    with open("config.json") as f:
        loaded = load(f)
    userStarts = bool(loaded["userStarts"])
    difficulty = int(loaded["difficulty1to8"])
    fontSize = int(loaded["fontSize"])
    app = App(root, userStarts, difficulty, fontSize)
    app.grid(column=0, row=0)
    root.mainloop()
