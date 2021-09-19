#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import math
import os
import packages.client.frames.style as style
from ...server import communication as comm


CONSTANTS = style.Constants
NUM_OF_ROUNDS = 2   # 8, temp, this should be stored somewhere else in order to be imported and visible for both client and server
WORKING_DIR = "\\".join(os.path.dirname(__file__).split("\\")[:-1])   # working directory of file: main.py


class Header(tk.Frame):
    ROUND_TEXT = "Round {} of " + str(NUM_OF_ROUNDS)
    ROUND_LABEL = None
    HIDDEN_TEXT = "{}"
    HIDDEN_WORD_LABEL = None
    TIMER_TEXT = "{}"
    TIMER_LABEL = None

    def __init__(self, master):
        """
        Constructor. Creates the header.
        :param master: <class tk.Frame>
        :return: None
        """
        self.master = master
        super().__init__(master=self.master, bg=CONSTANTS.Background.MAIN)
        self.create_gui()

    def create_gui(self):
        """
        Creates the gui widgets.
        :return: None
        """
        self.round_label = tk.Label(master=self, font=CONSTANTS.Font.NORMAL, bg=CONSTANTS.Background.MAIN)
        self.round_label.grid(row=1, column=1, padx=CONSTANTS.Padding.PAD10, pady=CONSTANTS.Padding.PAD10, sticky=tk.W)
        self.hidden_word_label = tk.Label(master=self, font=CONSTANTS.Font.NORMAL, bg=CONSTANTS.Background.MAIN)
        self.hidden_word_label.grid(row=1, column=2, pady=CONSTANTS.Padding.PAD10, sticky=tk.W)
        self.timer_label = tk.Label(master=self, font=CONSTANTS.Font.NORMAL, bg=CONSTANTS.Background.MAIN)
        self.timer_label.grid(row=1, column=3, padx=CONSTANTS.Padding.PAD10, pady=CONSTANTS.Padding.PAD10, sticky=tk.E)
        self.ROUND_LABEL = self.round_label
        self.HIDDEN_WORD_LABEL = self.hidden_word_label
        self.TIMER_LABEL = self.timer_label

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def update_(self, widget, value):
        """
        Updates the widget with given bumber.
        :param widget: <class tk.Label>
        :param value: str
        :return: None
        """
        try:
            widget.config(text=self.widget_text[widget].format(value))
        except RuntimeError as exception:
            print(f"[Error 63]\t\t{exception}")  # TODO: this happens when player is artist, and leaves during the turn, but not always?

    @property
    def widget_text(self):
        """
        Dictionary. Contains formatted text for each widget.
        :return: dict
        """
        return {
            self.ROUND_LABEL: self.ROUND_TEXT,
            self.HIDDEN_WORD_LABEL: self.HIDDEN_TEXT,
            self.TIMER_LABEL: self.TIMER_TEXT
        }


class PlayersList(tk.Frame):

    class PlayerBox(tk.Frame):
        USERNAME_TEXT = "#{}"
        SCORE_TEXT = "The score: {}"

        def __init__(self, master):
            """
            Constructor. Creates the player box.
            :param master: <class tk.Frame>
            :return: None
            """
            self.master = master
            super().__init__(master=self.master, bg=CONSTANTS.Background.MAIN)
            self.create_gui()

        def create_gui(self):
            """
            Creates the gui widgets.
            :return: None
            """
            self.username_label = tk.Label(master=self, font=CONSTANTS.Font.PLAYERLIST, bg=CONSTANTS.Background.MAIN)
            self.username_label.grid(row=1, column=1, padx=CONSTANTS.Padding.PAD5, pady=CONSTANTS.Padding.PAD1,
                                     sticky=tk.W)
            self.score_label = tk.Label(master=self, font=CONSTANTS.Font.SCORE, bg=CONSTANTS.Background.MAIN)
            self.score_label.grid(row=2, column=1, padx=CONSTANTS.Padding.PAD5, pady=CONSTANTS.Padding.PAD1,
                                  sticky=tk.W)

    def __init__(self, master):
        """
        Constructor. Creates the players list.
        :param master: <class tk.Frame>
        """
        self.master = master
        super().__init__(master=self.master, width=CONSTANTS.Width.PBOX, bg=CONSTANTS.Background.BORDER)
        self.propagate(False)
        blank_box = tk.Frame(master=self, width=CONSTANTS.Width.PBOX, bg=CONSTANTS.Background.MAIN)
        blank_box.pack(side=tk.BOTTOM, fill=tk.BOTH, pady=CONSTANTS.Padding.PAD5, expand=True)
        self.players = dict()

    def add(self, username):
        """
        Appends the player box, to the TOP.
        :param username: str
        :return: None
        """
        player_box = self.PlayerBox(master=self)
        player_box.username_label.config(text=player_box.USERNAME_TEXT.format(username))
        player_box.score_label.config(text=player_box.SCORE_TEXT.format('0'))
        player_box.pack(side=tk.TOP, pady=CONSTANTS.Padding.PAD5, fill=tk.BOTH, expand=False)
        self.players[username] = player_box

    def remove(self, username):
        """
        Removes the player box from the list.
        :param username: str
        :return: None
        """
        player_box = self.players[username]
        player_box.pack_forget()

    def update_score(self, leaderboard):
        """
        Updates the score for each player.
        :param leaderboard: str (<class Leaderboard> after evaluation
        :return: None
        """
        leaderboard = eval(leaderboard)
        for username in leaderboard:
            player_box = self.players[username]
            player_box.score_label.config(text=player_box.SCORE_TEXT.format(leaderboard[username]))


class Canvas(tk.Canvas):
    PEN_WIDTH = 40          # temp!
    PEN_COLOR = "black"     # temp!

    def __init__(self, master):
        """
        Constructor. Creates the canvas.
        :param master: <class tk.Frame>
        :return: None
        """
        self.master = master
        super().__init__(master=self.master)

        self.bind("<Button-1>", self.draw)
        self.bind("<B1-Motion>", self.draw)
        self.disable()

    def draw(self, event):
        """
        Draws the circle, with given point (center), current pen width and color.
        Creates the object string, draws it, and then sends to the server.
        :param event: <class tk.Event>
        :return: None
        """
        if not self.disabled:
            radius = self.PEN_WIDTH / 2
            a = round(math.sqrt(math.pow(radius, 2) / 2), 2)
            object_string = f"self.create_oval({event.x - a}, {event.y + a}, {event.x + a}, {event.y - a}, " \
                            f"fill='{self.PEN_COLOR}', outline='{self.PEN_COLOR}')"
            self.draw_from_string(value=object_string)
            comm.send(connection=self.master.connection, message=f"-image:{object_string}")

    def draw_from_string(self, value):
        """
        Draws the code from string.
        Method seems to be static, but value parameter contains string that has a few atributes, which contains
        parameter 'self'.
        :param value: str
        :return: None
        """
        eval(value)

    def disable(self):
        """
        Blocks the drawing.
        :return: None
        """
        self.disabled = True

    def enable(self):
        """
        Unlocks the drawing.
        :return: None
        """
        self.disabled = False

    def clear(self):
        """
        Clears the board.
        :return: None
        """
        self.delete(tk.ALL)


class PenConfig(tk.Frame):

    class ColorConfig(tk.Frame):
        COLORS = ["#000000", "#404040", "#ff0000", "#ff6a00", "#ffd800", "#b6ff00", "#4cff00", "#00ff21",
                  "#00ff90", "#00ffff", "#0094ff", "#0026ff", "#4800ff", "#b200ff", "#ff00dc", "#ff006e"]
        NUM_OF_ROWS = 2
        NUM_OF_COLS = 8

        def __init__(self, master):
            """
            Constructor. Creates the gui.
            :param master: <class tk.Frame>
            :return: None
            """
            self.master = master
            super().__init__(master=self.master, bg=CONSTANTS.Background.BORDER)
            self.create_gui()

        def create_gui(self):
            """
            Creates the gui widgets.
            :return: None
            """
            for index, color in enumerate(self.COLORS):
                tk.Button(master=self, bg=color, activebackground=color, width=CONSTANTS.Width.COLORBTN, height=CONSTANTS.Height.COLORBTN,
                          command=lambda c=color: self.on_color(c)).grid(
                    row=index // self.NUM_OF_COLS, column=index % self.NUM_OF_COLS,
                    padx=CONSTANTS.Padding.PAD1, pady=CONSTANTS.Padding.PAD1)

        def on_color(self, color):
            """
            Method is called when user selects the color.
            Sets the pen color.
            :param color: str
            :return: None
            """
            if not self.master.disabled:
                Canvas.PEN_COLOR = color

    class WidthConfig(tk.Frame):
        WIDTHS = [20, 30, 40, 50]   # temp, edit this later!
        NUM_OF_COLS = 4

        def __init__(self, master):
            """
            Constructor. Creates the gui.
            :param master: <class tk.Frame>
            :return: None
            """
            self.master = master
            super().__init__(master=self.master, bg=CONSTANTS.Background.MAIN)
            self.create_gui()

        def create_gui(self):
            """
            Creates the gui widgets.
            :return: None
            """
            img_path = "{}\\src\\images\\pen{}.png"
            for index, width in enumerate(self.WIDTHS):
                image = tk.PhotoImage(file=img_path.format(WORKING_DIR, index))
                button = tk.Button(master=self, image=image, command=lambda w=width: self.on_width(w))  # width=CONSTANTS.Width.COLORBTN, height=CONSTANTS.Height.COLORBTN,
                button.grid(row=1, column=index + 1, padx=CONSTANTS.Padding.PAD5, pady=CONSTANTS.Padding.PAD5)
                button.image = image

        def on_width(self, width):
            """
            Method is called when user selects the width.
            Sets the pen width.
            :param width: int
            :return: None
            """
            if not self.master.disabled:
                Canvas.PEN_WIDTH = width

    def __init__(self, master, canvas):
        """
        Constructor. Creates the gui.
        :param master: <class tk.Frame>
        :param canvas: <class Canvas>
        :return: None
        """
        self.master = master
        self.canvas = canvas
        super().__init__(master=self.master, bg=CONSTANTS.Background.MAIN)
        self.create_gui()
        self.disabled = True

    def create_gui(self):
        """
        Creates the gui widgets.
        :return: None
        """
        self.color_config = self.ColorConfig(master=self)
        self.width_config = self.WidthConfig(master=self)
        # print(f"DELETE PATH: {WORKING_DIR}\\src\\images\\delete.png")
        self.del_img = tk.PhotoImage(file=f"{WORKING_DIR}\\src\\images\\delete.png")
        self.del_btn = tk.Button(master=self, image=self.del_img, command=self.on_delete_all)
        self.del_btn.image = self.del_img

        self.color_config.grid(row=1, column=1, padx=CONSTANTS.Padding.PAD5, pady=CONSTANTS.Padding.PAD10, sticky=tk.W)
        self.width_config.grid(row=1, column=2, padx=CONSTANTS.Padding.PAD5, pady=CONSTANTS.Padding.PAD10, sticky=tk.E)
        self.del_btn.grid(row=1, column=3, padx=CONSTANTS.Padding.PAD5, pady=CONSTANTS.Padding.PAD10, sticky=tk.E)

    def disable(self):
        """
        Block the functionality.
        :return: None
        """
        self.disabled = True

    def enable(self):
        """
        Enabled the functionality.
        :return: None
        """
        self.disabled = False

    def on_delete_all(self):
        """
        Method is called when user click the delete button.
        :return: None
        """
        if not self.disabled:
            self.canvas.delete(tk.ALL)
            comm.send(connection=self.master.connection, message="-image:self.delete(tk.ALL)")


class Chat(tk.Frame):

    def __init__(self, master):
        """
        Constructor. Creates the gui.
        :param master: <class tk.Frame>
        :return: None
        """
        self.master = master
        super().__init__(master=self.master, bg=CONSTANTS.Background.BORDER)
        self.create_gui()
        self.enable()

    def create_gui(self):
        """
        Creates the gui widgets.
        :return: None
        """
        tk.Label(master=self, text="Chat", font=CONSTANTS.Font.NORMAL, bg=CONSTANTS.Background.MAIN).grid(
            row=1, column=1, sticky="ew")
        self.chat_box = tk.Text(master=self, font=CONSTANTS.Font.CHAT, bg=CONSTANTS.Background.MAIN, wrap=tk.WORD,
                                width=CONSTANTS.Width.CHAT)
        self.chat_box.grid(row=2, column=1, pady=CONSTANTS.Padding.PAD10, sticky="ns")
        self.chat_box.bind(sequence="<KeyPress>", func=lambda e: "break")   # read only
        self.msg_entry = tk.Entry(master=self, font=CONSTANTS.Font.MSG_ENTRY, bg=CONSTANTS.Background.MAIN)
        self.msg_entry.grid(row=3, column=1, sticky="sew")
        self.msg_entry.bind(sequence="<KeyPress-Return>", func=self.on_send)
        self.msg_entry.bind(sequence="<KeyPress>", func=self.on_key_press)
        self.msg_entry.bind(sequence="<Button-1>", func=self.on_mouse_press)

        self.grid_rowconfigure(2, weight=1)

    def disable(self):
        """
        Blocks the message entry.
        User cannot send the message anymore.
        :return: None
        """
        self.disabled = True

    def enable(self):
        """
        Unblocks the message entry.
        User can send the message.
        :return: None
        """
        self.disabled = False
        self.msg_entry.focus_set()

    def update_chat(self, username, message):
        """
        Updates the chat: adds the new message from the player.
        :param username: str
        :param message: str
        :return: None
        """
        self.chat_box.insert(tk.END, f"@{username} > {message}\n")

    def clear(self):
        """
        Cleares all the messages from the chat.
        :return: None
        """
        self.chat_box.delete(0.0, tk.END)

    def on_key_press(self, event=None):
        """
        Controls the keyboard press event.
        :param event: <class tk.Event>
        :return: None
        """
        if self.disabled:
            return

    def on_mouse_press(self, event=None):
        """
        Controls the mouse press event.
        :param event: <class tk.Event>
        :return: None
        """
        if self.disabled:
            return

    def on_send(self, event=None):
        """
        Sends the message to the server, but user must be the guesser.
        :param event: <class tk.Event>
        :return: None
        """
        # work on this, where should this be implemented (main thread loop?)
        if not self.disabled:
            comm.send(connection=self.master.connection, message=f"-isword:{self.msg_entry.get()}")
            self.msg_entry.delete(0, tk.END)


class GameFrame(tk.Frame):

    def __init__(self, master):
        """
        Constructor. Creates the gui.
        :param master: <class tk.Tk>
        """
        self.master = master
        super().__init__(master=self.master, bg=CONSTANTS.Background.BORDER)
        self.create_gui()
        self.connection = None

    def create_gui(self):
        """
        Creates the gui widgets.
        :return: None
        """
        self.header = Header(master=self)
        self.players_list = PlayersList(master=self)
        self.canvas = Canvas(master=self)
        self.pen_config = PenConfig(master=self, canvas=self.canvas)
        self.chat = Chat(master=self)

        self.header.grid(row=1, column=1, columnspan=3, padx=CONSTANTS.Padding.PAD5, pady=CONSTANTS.Padding.PAD5, sticky="ew")
        self.players_list.grid(row=2, rowspan=2, column=1, padx=CONSTANTS.Padding.PAD5, sticky="ns")
        self.canvas.grid(row=2, column=2, padx=CONSTANTS.Padding.PAD5, pady=CONSTANTS.Padding.PAD5, sticky="nsew")
        self.pen_config.grid(row=3, column=2, padx=CONSTANTS.Padding.PAD5, pady=CONSTANTS.Padding.PAD5, sticky="ew")
        self.pen_config.propagate(False)
        self.chat.grid(row=2, rowspan=2, column=3, padx=CONSTANTS.Padding.PAD5, pady=CONSTANTS.Padding.PAD5, sticky="ns")

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def set_connection(self, connection):
        """
        Sets the connection with the server.
        :param connection: <class socket.socket>
        :return: None
        """
        self.connection = connection
