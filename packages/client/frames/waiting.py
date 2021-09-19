#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import packages.client.frames.style as style

CONSTANTS = style.Constants


class WaitingFrame(tk.Frame):

    def __init__(self, master):
        """
        Constructor. Creates the gui.
        :param master: <class tk.Tk>
        """
        self.master = master
        super().__init__(master=self.master, bg=CONSTANTS.Background.MAIN)
        self.create_gui()

    def create_gui(self):
        """
        Creates the gui widgets.
        :return: None
        """
        self.text = tk.StringVar()
        tk.Label(master=self, textvariable=self.text, font=CONSTANTS.Font.NORMAL, bg=CONSTANTS.Background.MAIN).grid(
            row=1, column=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def config_text(self, text):
        """
        Configures the label text for a given parameter.
        :param text: str
        :return: None
        """
        self.text.set(text)
