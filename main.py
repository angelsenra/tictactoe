#! python3
from logging import (
    getLogger,
    DEBUG)
import tkinter as tk
from json import load

logger = getLogger("TicTacToe")
logger.setLevel(DEBUG)


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, relief="flat")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.config(bg="white")
    root.iconbitmap(default="icon.ico")
    root.geometry("100x100+0+0")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    with open("config.json") as f:
        loaded = load(f)
    userStarts = bool(loaded["userStarts"])
    difficulty = int(loaded["difficulty1to8"])
    app = App(root, )
    app.grid(column=0, row=0)
    root.mainloop()
