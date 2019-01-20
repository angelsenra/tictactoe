#! python3
import logging
import tkinter as tk
import tkinter.messagebox

import ai

FORMAT = "[%(asctime)s] [%(levelname)-8s] %(name)-4s: %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

V0 = " "
P1 = "X"
P2 = "O"
BUTTON_STYLE = {"bg": "#F0F0F0", "activebackground": "#F0F0F0", "bd": 7,
                "relief": "ridge", "overrelief": "groove", "text": V0}
CLICKED_STYLE = {"fg": "#FFF", "activeforeground": "#000",
                 "overrelief": "ridge"}
P2_STYLE = {**CLICKED_STYLE, "text": P2,
            "bg": "#00F", "activebackground": "#00F"}
P1_STYLE = {**CLICKED_STYLE, "text": P1,
            "bg": "#F00", "activebackground": "#F00"}

# Config:
RESOLUTION = (400, 400)
FONT = ("Arial", 100, "bold")
USER_STARTS = False  # If False the loser will start
DIFFICULTY = ai.MINIMAX


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.userTurn = USER_STARTS
        self.buttons = []
        for i in range(9):
            button = tk.Button(self, command=self.press(i), font=FONT)
            button.place(relx=i % 3 / 3, rely=i // 3 / 3, relwidth=1 / 3,
                         relheight=1 / 3, anchor="nw")
            self.buttons.append(button)
        self.new_game()

    def new_game(self):
        if USER_STARTS:
            self.userTurn = True
        self.board = ai.EMPTY.copy()
        for button in self.buttons:
            button.config(**BUTTON_STYLE)
        self.refresh()

    def move(self, button):
        human = self.userTurn
        self.buttons[button].config(**(P1_STYLE if human else P2_STYLE))
        self.board[button] = ai.HUMAN if human else ai.AI

        self.userTurn = not self.userTurn
        self.refresh()

    def ai_move(self):
        button = ai.move(self.board, False, DIFFICULTY)
        logger.info(f"AI chose {button}")
        self.move(button)

    def press(self, button):
        def wrapper():
            if ai.winner(self.board) or all(self.board):
                logger.error("The game is over")
                self.refresh()
            elif not self.userTurn:
                logger.error("It is not your turn yet")
            elif self.board[button]:
                logger.error("Could not choose that button")
            else:
                logger.info(f"You chose {button}")
                self.move(button)
        return wrapper

    def refresh(self):
        if ai.winner(self.board) or all(self.board):
            if tkinter.messagebox.askyesno("Replay", "Play Again?"):
                self.new_game()
        elif not self.userTurn:
            self.ai_move()


if __name__ == "__main__":
    ai.preload_minimax()
    # Root window
    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.config(bg="white")
    # Setting icon and resolution
    img = tk.Image("photo", file="icon.gif")
    root.tk.call("wm", "iconphoto", root._w, img)
    root.minsize(*RESOLUTION)
    # Root grid config
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # Creating App
    app = App(root)
    app.grid(column=0, row=0, sticky="NSEW")
    root.mainloop()
