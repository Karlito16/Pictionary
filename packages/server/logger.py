#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Logger(object):

    logger = True   # hardcoding

    def __str__(self):
        """
        Creates the output value.
        :return: str
        """
        return f"Logger: {self.logger}"

    @staticmethod
    def print(message):
        """
        Prints the message if it is allowed.
        :param message: str
        :return: None
        """
        if Logger.logger:
            print(message)
        return


def main():
    logger = Logger()
    print(logger)


if __name__ == '__main__':
    main()
