#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import packages.client.frames.style as style
from ...server import communication as comm


CONSTANTS = style.Constants


class SelectWordFrame(tk.Frame):

    def __init__(self, master):
        """
        Constructor. Creates the gui.
        :param master: <class tk.Tk>
        """
        self.master = master
        super().__init__(master=self.master, bg=CONSTANTS.Background.MAIN)
        self.create_gui()
        self.connection = None
        self.words = None
        self.buttons = []

    def create_gui(self):
        """
        Creates the gui widgets.
        :return: None
        """
        tk.Label(master=self, text="You are the artist!", font=CONSTANTS.Font.NORMAL,
                 bg=CONSTANTS.Background.MAIN).grid(
            row=1, column=1, columnspan=3, pady=CONSTANTS.Padding.PAD100, sticky="new")
        tk.Label(master=self, text="Select the word you want to draw:", font=CONSTANTS.Font.NORMAL,
                 bg=CONSTANTS.Background.MAIN).grid(
            row=2, column=1, columnspan=3, sticky="ew")

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def on_select(self, word_index):
        """
        Sends the selected word to the server.
        :param word_index: int
        :return: None
        """
        # self.set_word(word=self.words[word_index])
        comm.send(connection=self.connection, message=f"-choice:{self.words[word_index]}")

    def set_connection(self, connection):
        """
        Sets the connection with server.
        :param connection: <class socket.socket>
        :return: None
        """
        self.connection = connection

    def set_word(self, word):
        """
        # Sets the selected word. (EDIT: ???)
        :param word: str
        :return: None
        """
        # self.word = word

    def set_words(self, words):
        """
        Creates the buttons for words.
        :param words: str
        :return: None
        """
        self.words = words.split(",")
        self.buttons = []
        for index, word in enumerate(self.words):
            button = tk.Button(master=self, text=word, font=CONSTANTS.Font.SELWORD, command=lambda i=index: self.on_select(i))
            button.grid(row=3, column=index + 1, padx=CONSTANTS.Padding.PAD100, pady=CONSTANTS.Padding.PAD20)
            self.buttons.append(button)

    def clear(self):
        """
        Clears the buttons.
        :return: None
        """
        for button in self.buttons:
            button.grid_forget()
