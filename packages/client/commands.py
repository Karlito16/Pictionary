#!/usr/bin/env python3
# -*- coding: utf-8

from ..server import communication as comm


class Commands(object):

    def __init__(self, client, connection):
        """
        Constructor. Class contains all commands that must be executed if server/client request the same.
        :param client: <class Client>  (inherited <class client>)
        :param connection: <class socket.socket>
        """
        self.client = client
        self.connection = connection

    def get_chat(self, value):
        """
        Gets the message that needs to be updated in the chat.
        Message example: "John,Guessed the word"
        :param value: str
        :return: None
        """
        username, message = value.split(",")
        self.client.GAME_FRAME.chat.update_chat(username=username, message=message)

    def get_dword(self, drawing_word):
        """
        Gets the drawing word. (ONLY ARTIST)
        Shows it on the top of the screen.
        :param drawing_word: str
        :return: None
        """
        self.client.GAME_FRAME.header.update_(widget=self.client.GAME_FRAME.header.HIDDEN_WORD_LABEL, value=drawing_word)

    def get_end(self, leaderboard):
        """
        Gets the information about game ending.
        Also forwards the leaderboard which will be shown on the end frame.
        Shows the end frame.
        :param leaderboard: str
        :return: None
        """
        self.client.END_FRAME.create_table(values=leaderboard)
        self.client.show(frame=self.client.END_FRAME)

    def get_gamestat(self, value):
        """
        Gets the game status.
        If True, sends the request: -gameinfo.
        Otherwise, shows the waiting frame.
        :param value: str
        :return: None
        """
        if eval(value):
            comm.send(connection=self.connection, message="-gameinfo:")
            self.client.game_running = True
        else:
            self.client.WAITING_FRAME.config_text(text="Waiting for players...")
            self.client.show(frame=self.client.WAITING_FRAME)

    def get_hword(self, hidden_word):
        """
        Gets the hidden word. Shows it on the top of the screen. (ONLY FOR GUESSERS)
        :param hidden_word: str
        :return: None
        """
        self.client.GAME_FRAME.header.update_(widget=self.client.GAME_FRAME.header.HIDDEN_WORD_LABEL, value=hidden_word)

    def get_image(self, image):
        """
        Gets and forwards the code for drawing.
        This way, user gets updated picture.
        :param image: str
        :return: None
        """
        self.client.GAME_FRAME.canvas.draw_from_string(value=image)
        # TODO: what if artist deletes all?

    def get_isword(self, boolean):
        """
        Gets the confirmation if user guessed the word or not.
        Blocks the entry box if he guessed the word until the next turn.
        :param boolean: str (bool after evaluation)
        :return: None
        """
        if eval(boolean):
            self.client.GAME_FRAME.chat.disable()

    def get_join(self, username):
        """
        Gets the information about new player who has joined the game.
        Forwards this to the game frame which will then update the players list.
        :param username: str
        :return: None
        """
        self.client.GAME_FRAME.players_list.add(username=username)

    def get_leaderboard(self, leaderboard):
        """
        Gets the leaderboard (after each turn) and forwards it to the game frame
        which will then update the score for each player.
        :param leaderboard: str
        :return: None
        """
        self.client.GAME_FRAME.players_list.update_score(leaderboard=leaderboard)

    def get_left(self, username):
        """
        Gets the information about new player who has joined the game.
        Forwards this to the game frame which will then update the players list.
        # TODO: Consider changing format of the commands -join/-left: we delete player by its username, but what if we have two players with the same username???
        :param username: str
        :return: None
        """
        self.client.GAME_FRAME.players_list.remove(username=username)

    def get_result(self, value):
        """
        Gets the word and leaderboard, inside the parameter value.
        Forwards it to the results frame.
        :param value: str
        :return: None
        """
        # word, leaderboard = value.split(",")   => old
        word, leaderboard = value.split("|")   # => new
        self.client.RESULTS_FRAME.create_table(word=word, leaderboard=leaderboard)
        self.client.show(frame=self.client.RESULTS_FRAME)

    def get_role(self, role):
        """
        Gets the role for upcoming turn.
        Prepares the multiple frames for new turn.
        :param role: str
        :return: None
        """
        self.client.SELECT_WORD_FRAME.clear()
        self.client.GAME_FRAME.canvas.clear()
        self.client.GAME_FRAME.chat.clear()
        self.client.role = role
        if self.client.role == "artist":
            self.client.GAME_FRAME.chat.disable()
            self.client.GAME_FRAME.canvas.enable()
            self.client.GAME_FRAME.pen_config.enable()
            # self.client.GAME_FRAME.pen_config.show()  # instead, we will disable and enable
        else:
            self.client.GAME_FRAME.chat.enable()
            self.client.GAME_FRAME.canvas.disable()
            self.client.GAME_FRAME.pen_config.disable()
            self.client.WAITING_FRAME.config_text(text="Waiting for artist to select the word...")
            self.client.show(frame=self.client.WAITING_FRAME)

    def get_round(self, round_):
        """
        Gets the round number.
        :param round_: str
        :return: None
        """
        self.client.GAME_FRAME.header.update_(widget=self.client.GAME_FRAME.header.ROUND_LABEL, value=round_)

    def get_start(self):
        """
        Start of the new turn.
        Shows the game frame.
        :return: None
        """
        self.client.show(frame=self.client.GAME_FRAME)

    def get_time(self, time_):
        """
        Gets the time remaining.
        Forwards the time to the game frame which
        will then update the time on the screen.
        :param time_: str
        :return: None
        """
        self.client.GAME_FRAME.header.update_(widget=self.client.GAME_FRAME.header.TIMER_LABEL, value=time_)

    def get_timeisup(self):
        """
        End of the turn. Waiting for results...
        :return:
        """
        # useful?
        pass

    def get_word(self):
        """
        Replaced with method 'get_dword'.
        :return: None
        """
        pass

    def get_words(self, words):
        """
        Gets the string of words, separated by comma.
        Shows the select word frame.
        :return: None
        """
        select_word_frame = self.client.SELECT_WORD_FRAME
        select_word_frame.set_words(words=words)
        self.client.show(frame=select_word_frame)
