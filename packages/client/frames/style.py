#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Constants(object):

    class Background(object):
        MAIN = "white"
        BORDER = "black"

    class Foreground(object):
        MAIN = "black"

    class Font(object):
        FONT = "Calibri"
        TITLE = (FONT, 40, "bold italic")
        NORMAL = (FONT, 24, "bold")
        SCORE = (FONT, 12, "italic")
        CHAT = (FONT, 10)
        MSG_ENTRY = (FONT, 14)
        RESULTS = (FONT, 18, "bold")
        PLAYERLIST = (FONT, 15, "bold")
        SELWORD = (FONT, 16, "bold")

    class Padding(object):
        PAD1 = 1
        PAD5 = 5
        PAD10 = 10
        PAD20 = 20
        PAD50 = 50
        PAD100 = 100

    class Width(object):
        PBOX = 150
        COLORBTN = 1
        CHAT = 30

    class Height(object):
        PBOX = 0
        PENCONFIG = 150
        COLORBTN = 1
