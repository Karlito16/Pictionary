#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import packages.server.communication as comm


class Constants(object):

    ALL = "all"


class Leaderboard(Constants):

    def __init__(self, sequence=None):
        """
        Constructor for the class 'Leaderboard'.
        Body:
                {<class Player>: int}
        :param sequence: list :: [<class Player>]
        """
        self._dict = dict()
        if sequence is not None:
            # Using the class type as a key because it is possible to have two players with the same name.  =>  NOT ANYMORE
            # Maybe this should be restricted at the very begin of the program, when client joins the game. =>  YES!!!
            for player in sequence:
                self._dict[player.username] = 0

    def __delitem__(self, key):
        del self._dict[key]

    def __getitem__(self, item):
        try:
            return self._dict[item]
        except KeyError:
            return

    def __iter__(self):
        return iter(self._dict)

    def __repr__(self):
        return self.__str__()

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __str__(self):
        return str(self._dict)

    def update(self, leaderboard):
        """
        Updates the leaderboard with values from another leaderboard.
        :param leaderboard: <class Leaderboard>
        :return: None
        """
        for username in leaderboard:
            # possibility that player left the game while turn was still on
            if username in self._dict.keys():
                self._dict[username] += leaderboard[username]
                # player.update_score(score=leaderboard[player])  # work on this, will it even be used?

    def players(self):
        """
        Returns the list of players.
        :return: list :: [<class Player>]
        """
        # return list(self._dict)   => not anymore, as we use usernames for keys instead

    def send(self, sequence):
        """
        Sorts and sends sorted leaderboard to the all players named in the sequence.
        If sequence is ALL, then sends to the all players.
        :param sequence: list :: [<class Player>]
        :return: None
        """
        self.sort()
        message = f"-leaderboard;{self._dict}"   # we need to do this replacement because dict has ':' in it's constructure
        comm.send_to_all(sequence=sequence, message=message)

    def sort(self):
        """
        Sorts the leaderboard by scores.
        :return: None
        """
        scores = []
        items = self._dict.items()
        for _, score in items:
            scores.append(score)
        scores = qsort(scores)
        self._dict = {}
        for score in scores:  # we can have two or more players with same the score
            for index, item in enumerate(items):
                if item[1] == score:
                    self._dict[item[0]] = item[1]


def qsort(lst):  # [3, 2, 4, 1, 5]
    """
    Takes the list and sorts it (descending order).
    It also removes identical elements.
    :param lst: list
    :return: list
    """
    if not lst:
        return []
    pivot = lst[len(lst) // 2]
    ahead = [x for x in lst if x > pivot]
    after = [x for x in lst if x < pivot]
    return [qsort(ahead)] + [pivot] + [qsort(after)]
