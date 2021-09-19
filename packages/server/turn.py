#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import packages.server.communication as comm
import packages.server.leaderboard as lboard


WORDS = ["apple", "pen", "house", "skycreeper", "school", "mice", "planet", "sky diving", "mud", "blue sky"]    # temp!
DRAWING_TIME = 10   # 80
SELECT_WORD_TIME = 5
WATCH_RESULTS_TIME = 5
MAX_POINTS = 100
POINTS_PER_GUESS = 10
SECOND = 1


class Turn(object):
    CONDITIONS = {
        None: "True",
        "drawing": "not self.num_of_guesses == self.game.num_of_players and self.artist.connected",
        "word": "self.word is None"
    }

    def __init__(self, game, artist, guessers):
        """
        Constructor for class Turn.
        :param artist: <class Player>
        :param guessers: list :: [<class Players>]
        """
        self.game = game
        self.artist = artist
        self.guessers = guessers
        self.word = self.hword = None   # hword = hided word
        self.words = []
        self.num_of_guesses = 0
        # this will be sent to each player after each turn, so they can recreate leaderboard from this object
        self.leaderboard = lboard.Leaderboard(sequence=self.game.players)

    def check_selection(self):
        """
        Checks if player selected the word.
        :return: bool
        """
        if self.word is None:
            return False
        return True

    def check_word(self, player, word):
        """
        Checks the player's guess. If he guessed, method returns True, otherwise False.
        Method also implements the scoring system.
        :param player: <class Player>
        :param word: str
        :return: bool
        """
        if word == self.word:
            self.score(player=player)
            return True
        return False

    def countdown(self, seconds, condition_key=None):
        """
        Counts down the time. Parameter 'condition_key' defines which condition method
        needs to be tracked in order to successfully complete countdown.
        At the end of the countdown, method sends a message that there is no time left, respectively.
        :param seconds: int
        :param condition_key: str (default is None)
        :return: None
        """
        condition = self.CONDITIONS[condition_key] + " and seconds > 0"
        while eval(condition):
            time.sleep(SECOND)
            seconds -= SECOND
            if condition_key == "drawing":
                comm.send_to_all(sequence=self.game.players, message=f"-time:{seconds}")

        if condition_key == "drawing":
            comm.send_to_all(sequence=self.game.players, message="-timeisup:")

    def hide_word(self):  # blue sky
        """
        Creates hidden word.
        Example: (blue sky -> _ _ _ _   _ _ _)
        :return: None
        """
        hided_word = ""
        for char in self.word:
            if char == ' ':
                hided_word += "  "
            else:
                hided_word += "_ "
        self.hword = hided_word

    def inform_role(self):
        """
        Method informs the players about their role for this turn.
        :return: None
        """
        comm.send(connection=self.artist.connection, message="-role:artist")
        comm.send_to_all(sequence=self.guessers, message="-role:guesser")

    def gen_words(self):
        """
        Generates three randomly selected words from word list.
        :return: None
        """
        self.words = random.sample(WORDS, 3)

    def gen_word(self):
        """
        Generates one word from previously generated list of three randomly selected words.
        This will happen only if player doesn't select the word on his own.
        :return: None
        """
        self.word = random.choice(self.words)

    def get_word(self):
        """
        Gets the word which will be the one artist will draw, and guesssers will guess.
        :return: None
        """
        self.gen_words()
        comm.send(connection=self.artist.connection, message="-words:{}".format(','.join(self.words)))
        self.countdown(seconds=SELECT_WORD_TIME, condition_key="word")
        if not self.check_selection():
            self.gen_word()     # generates the random word, in case artist didn't choose the word
        comm.send(connection=self.artist.connection, message=f"-dword:{self.word}")  # sends him the word for drawing
        self.hide_word()
        comm.send_to_all(sequence=self.guessers, message=f"-hword:{self.hword}")

    def score(self, player):
        """
        Increases the total score for given player. Also updates the leaderboard for current turn.
        TODO: Try and implement decorator with this method and methods 'on_guess' and 'score_artist'!
        :param player: <class Player>
        :return: None
        """
        # updates the score for player
        player_score = MAX_POINTS - self.num_of_guesses * (MAX_POINTS // self.game.num_of_players)
        self.leaderboard[player.username] = player_score
        player.score += player_score
        self.num_of_guesses += 1

    def score_artist(self):
        """
        Scores the artist.
        :return: None
        """
        # '<=' because some players can leave the game after they guessed the word
        if not self.game.num_of_players <= self.num_of_guesses:
            score = self.num_of_guesses * POINTS_PER_GUESS
            self.leaderboard[self.artist.username] += score
            self.artist.score += score

    def show_result(self):
        """
        Method sends the word that has been guessed as well as the leaderboard for that turn.
        It also calls the countdown method, and scores the artist for this turn.
        :return: None
        """
        self.score_artist()
        # comma was used to separate the parameters, but since dictionary has commas in it's structure, we decided to use | instead
        comm.send_to_all(sequence=self.game.players, message=f"-result;{self.word}|{self.leaderboard}")
        self.countdown(seconds=WATCH_RESULTS_TIME)

    def start(self):
        """
        Starts the new turn.
        Sends the message for turn start.
        Calls the countdown method.
        :return: None
        """
        comm.send_to_all(sequence=self.game.players, message="-start:")
        self.countdown(seconds=DRAWING_TIME, condition_key="drawing")
