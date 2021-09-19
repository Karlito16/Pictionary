#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import packages.server.communication as comm
import packages.server.leaderboard as lboard
import packages.server.player as player
import packages.server.round as round_
import packages.server.turn as turn

RUNNING_SLEEP = 0.0001
CONNECTION_CLOSE_SLEEP = 0.2
NUMBER_OF_ROUNDS = 1    # 8


class Game(object):

    def __init__(self, server):
        """
        Constructor for class Game.
        :param server: <class socket>
        """
        self.server = server
        self.players = []
        self.game_runnig = False
        self.round = round_.Round()
        self.leaderboard = lboard.Leaderboard()

    def end(self):
        """
        Ends the game.
        :return: None
        """
        for player_ in self.players:
            # time.sleep(SEND_SLEEP)
            comm.send(connection=player_.connection, message=f"-end;{self.leaderboard}")
            player_.disconnect()
            time.sleep(CONNECTION_CLOSE_SLEEP)  # prevents the [Error 79]	[WinError 10053] An established connection was aborted by the software in your host machine
            player_.connection.close()  # [Error 79] because while loop in 'client_trace' is sill running and trying to receive new message
        # self.game_runnig = False
        # self.players = []
        self.__init__(server=self.server)

    def loop(self):
        """
        Starts the game loop (Thread, started from server.py program).
        Controls the game task flow.
        :return: None
        """
        
        while True:     # while server is running
            time.sleep(RUNNING_SLEEP)
            
            while not self.game_runnig:
                time.sleep(RUNNING_SLEEP)
                if self.server.connections > 1:
                    self.game_runnig = True
                    # basically, this will be sent to the first two players
                    # comm.send_to_all(sequence=self.players, message=f"-gamestat:{self.game_runnig}")
                    
            while self.round <= NUMBER_OF_ROUNDS:
                time.sleep(RUNNING_SLEEP)
                self.round.send(sequence=self.players)
                
                artist_index = 0
                while artist_index < self.num_of_players:
                    self.turn = turn.Turn(game=self, artist=self.get_artist(artist_index), guessers=self.get_guessers(artist_index))
                    self.turn.inform_role()     # is this needed?

                    self.turn.get_word()

                    self.turn.start()

                    self.turn.show_result()

                    self.leaderboard.update(leaderboard=self.turn.leaderboard)

                    self.leaderboard.send(sequence=self.players)

                    artist_index += 1
                
                self.round.new()

            print("!!END!!")
            self.end()

    def get_artist(self, index):
        """
        Returns the player who is selected to be the artist for upcoming turn.
        Index represents next expression: self.players.index(artist)
        :param index: int
        :return: <class Player>
        """
        return self.players[index]

    def get_guessers(self, index):
        """
        Returns the list which represents players who are guessing for upcoming turn.
        Index represents next expression: self.players.index(artist)
        :param index: int
        :return: list
        """
        return self.players[:index] + self.players[index + 1:]

    def get_ply_by_conn(self, connection):
        """
        Returns the player object which contains given connection object.
        :param connection: <class socket>
        :return: <class Player>
        """
        for player_ in self.players:
            if player_.connection == connection:
                return player_

    @property
    def num_of_players(self):
        """
        Returns the number of players who are currently in the game.
        TODO: This will probably break if someone joins/leaves the game at the time of drawing, which
        TODO: will then break the scoring system, as it depends on number of num_of_players!!!
        :return: None
        """
        return len(self.players)

    def player_add(self, connection, address):
        """
        Creates player instance and appends it to the player list.
        Also requires username for successfull connection.
        :param connection: <class socket>
        :param address: dict
        :return: bool
        """
        username = comm.receive(connection=connection, command_key="-username")
        if username:
            player_ = player.Player(username, connection, address)
            self.players.append(player_)
            self.server.client_join_info(username=username)
            comm.send_to_all(sequence=self.players, message=f"-join:{username}")
            comm.send(connection=connection, message=f"-gamestat:{self.game_runnig}")
            self.leaderboard[player_.username] = 0
            return True
        else:
            # otherwise, keeps the player connected, but does not add him to the game
            return False

    def player_remove(self, connection):
        """
        Removes the player from the list of players and the leaderboard.
        :param connection: socket object
        :return: None
        """
        for index, player_ in enumerate(self.players):
            if player_.connection == connection:
                del self.leaderboard[player_.username]
                self.players.pop(index)
                # what if player leaves during the turn and what if he was the artist?
                connection.close()      # test this, sometimes it throws ConnectionAbortError in method self.listen
                player_.disconnect()
                self.server.client_left_info(username=player_.username)
                # time.sleep(SEND_SLEEP)
                comm.send_to_all(sequence=self.players, message=f"-left:{player_.username}")

    def player_inform(self, connection):
        """
        Informs the player who has joined during the game about current round and so on.
        :param connection: <class socket>
        :return: None
        """
        # time will be sent through countdown method
        # image will be sent automatically

        player_ = self.get_ply_by_conn(connection=connection)
        self.round.send(sequence=[player_])

        # the code above will add already joined players to the players list of the recently joined player
        for player__ in self.players:
            if player__.connection != connection:
                comm.send(connection=connection, message=f"-join:{player__.username}")

        self.leaderboard.send(sequence=[player_])

        # sends him the role    -   what if he should be the artist?
        comm.send(connection=connection, message="-role:guesser")
