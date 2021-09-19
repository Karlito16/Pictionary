#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading as thread
import packages.server.communication as comm
import packages.server.game as game
from packages.server.logger import Logger

PORT = 10000
MAX_NUM_OF_CONNECTIONS = 8


class Server(socket.socket):

    def __init__(self, host, port):
        """
        Constructor. Creates connection with socket.
        :param host: str
        :param port: int
        """
        super().__init__()
        self.host = host
        self.port = port
        self.bind((self.host, self.port))
        self.listen(5)
        self.game = game.Game(server=self)

    @property
    def connections(self):
        return len(self.game.players)

    def client_accept(self):
        """
        Accepts the client and adds him to the list of players.
        :return: <class socket>
        """
        connection, address = self.accept()
        self.game.player_add(connection, address)
        return connection

    @staticmethod
    def client_join_info(username):
        """
        :param username: str
        :return: None
        """
        # print(f"[INFO]\t\tInfo: Client {username} joined")
        Logger.print(f"[INFO]\t\tInfo: Client {username} joined")
        return

    @staticmethod
    def client_left_info(username):
        """
        :param username: str
        :return: None
        """
        # print(f"[INFO]\t\tInfo: Client {username} left")
        Logger.print(f"[INFO]\t\tInfo: Client {username} left")
        return

    def client_trace(self, connection):
        """
        While loop; all messages that çlient sends arrives here.
        :param connection: <class socket>
        :return: None
        """
        player = self.game.get_ply_by_conn(connection=connection)

        while player.connected:
            try:
                command_key, value = comm.receive(connection=connection)
            except ValueError as err:
                # print(f"Player connected: {player.connected}")
                pass    # this happens at the end of the game, when disconnecting players - temp solution?
            except Exception as err:        # TODO: replace Exception with ConnectionAbortError - TEST THIS
                Logger.print(f"[Error 73] {err}")
                break   # thread ends here
            else:
                if command_key == "-choice":
                    # artist selected the word
                    self.game.turn.word = value

                elif command_key == "-gameinfo":
                    # player who joined the game while the same has already began, requests must informations
                    self.game.player_inform(connection=connection)

                elif command_key == "-image":
                    # for updating the current image
                    comm.send_to_all(sequence=self.game.turn.guessers, message=f"{command_key}:{value}")

                elif command_key == "-isword":
                    # guesser tries to guess the word
                    player_instance = self.game.get_ply_by_conn(connection=connection)
                    is_word = self.game.turn.check_word(player=player_instance, word=value)
                    comm.send(connection=connection, message=f"{command_key}:{str(is_word)}")
                    message = "-chat:{},{}".format(player_instance.username, {True: "Guessed the word!", False: value}[is_word])
                    comm.send_to_all(sequence=self.game.players, message=message)

                elif command_key == "-left":
                    # player left the game
                    self.game.player_remove(connection=connection)
                    # break   # this ends the while loop (should fix ERROR 37)

    def start_game_thread(self):
        """
        This method starts game loop thread.
        :return: None
        """
        thread.Thread(target=self.game.loop).start()

    def wait(self):
        """
        Waits for new client to join. Accepts him and creates a new thread for comminucation with him.
        :return: None
        """
        while True:     # TODO: replace expression "while True" with "while <some condition>"
            if self.connections < MAX_NUM_OF_CONNECTIONS:
                # print("[Waiting...]\t\tStatus: Waiting for players")
                Logger.print("[Waiting...]\t\tStatus: Waiting for players")
                connection = self.client_accept()
                thread.Thread(target=self.client_trace, args=(connection,)).start()


def main():
    server = Server(host=socket.gethostname(), port=PORT)  # TODO: Check what exactly you need to send as host and port; temp solution
    server.start_game_thread()      # currently, this will only produce one game
    server.wait()


if __name__ == '__main__':
    main()
