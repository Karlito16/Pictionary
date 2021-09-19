#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import packages.client.frames.style as style

CONSTANTS = style.Constants


class JoinFrame(tk.Frame):

    USERNAME_SIZE = 15

    def __init__(self, master):
        """
        Constructor. Creates the gui.
        :param master: <class tk.Tk>
        """
        self.master = master
        super().__init__(master=self.master, bg=CONSTANTS.Background.MAIN, width=900, height=675)
        self.create_gui()
        self.username = self.join = None

    def create_gui(self):
        """
        Creates the gui widgets.
        :return: None
        """
        tk.Label(master=self, text="Pictionary", font=CONSTANTS.Font.TITLE, bg=CONSTANTS.Background.MAIN).grid(
            row=1, column=1, columnspan=3, pady=CONSTANTS.Padding.PAD20, sticky=tk.N)
        tk.Label(master=self, text="Username: ", font=CONSTANTS.Font.NORMAL, bg=CONSTANTS.Background.MAIN).grid(
            row=2, column=1, padx=CONSTANTS.Padding.PAD20, pady=CONSTANTS.Padding.PAD50, sticky=tk.W)
        self.entry_var = tk.StringVar()
        tk.Entry(master=self, textvariable=self.entry_var, font=CONSTANTS.Font.NORMAL, bg=CONSTANTS.Background.MAIN, width=20).grid(
            row=2, column=2, columnspan=2, padx=CONSTANTS.Padding.PAD20, sticky=tk.W)
        tk.Button(master=self, text="JOIN", font=CONSTANTS.Font.NORMAL, command=self.on_join).grid(
            row=3, column=3, padx=CONSTANTS.Padding.PAD50, pady=CONSTANTS.Padding.PAD50, sticky="se")

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def on_join(self):
        """
        Sets the attribute 'join' to the valid boolean value, depending on the validity of entered username.
        :return: None
        """
        self.username = self.entry_var.get()[:self.USERNAME_SIZE]
        if self.username:
            self.join = True
        else:
            self.join = False
