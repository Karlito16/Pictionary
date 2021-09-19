#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
import time
from packages.server.logger import Logger


CODING = "UTF-8"
BUFSIZE = 1024  # TODO: can be reduced! chech this later! optimize!
SEND_SLEEP = 0.1
RECEIVE_SLEEP = 0.0001


def sending_info(func):
    functools.wraps(func)

    def sending_info_wrapper(*args, **kwargs):
        # print(f"[Sending...]\t\tMessage: {kwargs['message']}")
        Logger.print(message=f"[Sending...]\t\tMessage: {kwargs['message']}")
        time.sleep(SEND_SLEEP)
        return func(*args, **kwargs)

    return sending_info_wrapper


@sending_info
def send(connection, message):
    """
    Sending the message.
    :param connection: <class socket>
    :param message: string
    :return: bool
    """
    try:
        connection.send(message.encode(CODING))
    except Exception as exception:
        # print(f"[Error 37]\t{exception}\nFailed to send the message.")
        Logger.print(message=f"[Error 37]\t{exception}\nFailed to send the message.")
        return False
    else:
        return True


def send_to_all(sequence, message):
    """
    Sending the message to the all members of the sequence.
    :param sequence: list :: [<class Player>]
    :param message: str
    :return: None
    """
    for player in sequence:
        send(connection=player.connection, message=message)


def receive_info(func):
    functools.wraps(func)

    def receive_info_wrapper(*args, **kwargs):
        if 'command_key' in kwargs.keys():
            value = func(*args, **kwargs)
            items = kwargs.items()
            for cmd_key, value_ in items:
                if value_ == value:
                    # print(f"[Received]\t\t\tMessage: {cmd_key}:{value}")
                    Logger.print(message=f"[Received]\t\t\tMessage: {cmd_key}:{value}")
            return value
        else:
            cmd_key, value = func(*args, **kwargs)
            # print(f"[Received]\t\tMessage: {cmd_key}:{value}")
            Logger.print(message=f"[Received]\t\tMessage: {cmd_key}:{value}")
            return cmd_key, value

    return receive_info_wrapper


@receive_info
def receive(connection, command_key=None):
    """
    Gets the message from the connection object according to command key.
    If command key is None, function returns full message. Otherwise,
    for example, if player sends his username, server wants to read it.
    Then, command key is "-username". If he succeedes to read it,
    returns value, otherwise "" (False).
    :param connection: <class socket>
    :param command_key: string (default is None)
    :return: str or list :: [str, str]
    """
    try:
        message = connection.recv(BUFSIZE).decode(CODING)
    except Exception as exception:
        # print(f"[Error 79]\t{exception}\nFailed to receive a message.")
        Logger.print(message=f"[Error 79]\t{exception}\nFailed to receive a message.")
        return
    else:
        if command_key is None:
            if "-result" in message or "-leaderboard" in message or "-end" in message:
                return message.split(";")   # because dictionary has ':' in his syntax
            else:
                return message.split(":")
        else:
            cmd_key, value = message.split(":")
            if cmd_key == command_key:
                return value
            return ""
