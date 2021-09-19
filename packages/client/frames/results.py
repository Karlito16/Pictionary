#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import packages.client.frames.style as style

CONSTANTS = style.Constants


class ResultsFrame(tk.Frame):
    WORD_LABEL = "Word: {}"

    def __init__(self, master):
        """
        Constructor. Creates the gui.
        :param master: <class tk.Tk>
        """
        self.master = master
        super().__init__(master=self.master, bg=CONSTANTS.Background.MAIN)
        self.create_gui()
        self.table = []

    def create_gui(self):
        """
        Creates the gui widgets.
        :return: None
        """
        self.word_var = tk.StringVar()
        tk.Label(master=self, textvariable=self.word_var, font=CONSTANTS.Font.NORMAL, bg=CONSTANTS.Background.MAIN).grid(
            row=1, column=1, columnspan=5, pady=CONSTANTS.Padding.PAD50)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def create_table(self, word, leaderboard):
        """
        Creates the labels which contains:
            Position: Username: The Score
        :param word: str
        :param leaderboard: str (<class Leaderboard> after evaluation)
        :return: None
        """
        leaderboard = eval(leaderboard)
        self.word_var.set(self.WORD_LABEL.format(word))
        for position, username in enumerate(leaderboard):
            pos_label = tk.Label(master=self, text=f"{position + 1}.", font=CONSTANTS.Font.RESULTS,
                                 bg=CONSTANTS.Background.MAIN)
            username_label = tk.Label(master=self, text=f"{username}", font=CONSTANTS.Font.RESULTS,
                                      bg=CONSTANTS.Background.MAIN)
            score_label = tk.Label(master=self, text=f"{leaderboard[username]}", font=CONSTANTS.Font.RESULTS,
                                   bg=CONSTANTS.Background.MAIN)
            pos_label.grid(row=position + 3, column=2, sticky=tk.W)
            username_label.grid(row=position + 3, column=3, padx=CONSTANTS.Padding.PAD10, pady=CONSTANTS.Padding.PAD5, sticky=tk.W)
            score_label.grid(row=position + 3, column=4, sticky=tk.W)
            self.table.append((pos_label, username_label, score_label))

    def clear_table(self):
        """
        Clears the labels from the frame.
        :return: None
        """
        for row in self.table:
            for label in row:
                label.grid_forget()
        self.table = []
