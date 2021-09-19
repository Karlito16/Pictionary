#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import packages.server.communication as comm


class Round(int):

    def __init__(self):
        self._round = 1
        super().__init__()

    def __le__(self, other):
        """
        Special method for less or equals to condition.
        :param other: int
        :return: bool
        """
        if self._round <= other:
            return True
        return False

    def new(self):
        """
        Increases the round number.
        :return: None
        """
        self._round += 1

    def send(self, sequence):
        """
        Sends the round number to the all members of the sequence.
        :param sequence: list :: [<class Player>]
        :return: None
        """
        comm.send_to_all(sequence=sequence, message=f"-round:{self._round}")
