#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Player(object):

    def __init__(self, username, connection, address):
        self.username = username
        self.connection = connection
        self.address = address
        self.connected = True
        self.score = 0

    def update_score(self, score):
        self.score += score
