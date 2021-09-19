#!/usr/bin/env python3
# -*- coding: utf-8

import threading as thread
import time
import tkinter as tk
import socket
import packages.client.commands as commands
import packages.client.frames as frames
import packages.server.communication as comm
from packages.server.logger import Logger

PORT = 10000
RUNNING_SLEEP = 0.0001


class Window(tk.Tk):
    JOIN_FRAME = None
    WAITING_FRAME = None
    SELECT_WORD_FRAME = None
    GAME_FRAME = None
    RESULTS_FRAME = None
    END_FRAME = None
    ACTIVE_FRAME = None

    def __init__(self):
        """
        Constructor. Inits all frames.
        """
        super().__init__()
        self.title("Pictionary")
        self.config(bg=frames.WIN_BACKGROUND, width=frames.WIN_WIDTH, height=frames.WIN_HEIGHT)
        # self.resizable(width=False, height=False)
        self.propagate(False)
        self.init_frames()

    def init_frames(self):
        """
        Initialization.
        :return: None
        """
        self.JOIN_FRAME = frames.join.JoinFrame(master=self)
        self.WAITING_FRAME = frames.waiting.WaitingFrame(master=self)
        self.SELECT_WORD_FRAME = frames.selword.SelectWordFrame(master=self)
        self.GAME_FRAME = frames.game.GameFrame(master=self)
        self.RESULTS_FRAME = frames.results.ResultsFrame(master=self)
        self.END_FRAME = frames.end.EndFrame(master=self)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def show(self, frame):
        """
        Shows the frame.
        :param frame: <class tk.Frame>
        :return: None
        """
        if self.ACTIVE_FRAME is not None:
            self.ACTIVE_FRAME.pack_forget()
        frame.pack(fill=tk.BOTH, padx=frames.WIN_PADDING, pady=frames.WIN_PADDING, expand=frames.WIN_EXPAND)
        frame.propagate(False)      # needed?
        self.ACTIVE_FRAME = frame


class Client(Window):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        super().__init__()

        self.connection = socket.socket()
        # important, used for sending the current image and user guess! (-image: | -isword:)
        self.GAME_FRAME.set_connection(connection=self.connection)
        # important, used for sending the selected word! (-choice:)
        self.SELECT_WORD_FRAME.set_connection(connection=self.connection)

        # self._test_frame()
        self.show(frame=self.JOIN_FRAME)
        self.protocol("WM_DELETE_WINDOW", self.end)

        self.commands = commands.Commands(client=self, connection=self.connection)

        self.thread = thread.Thread(target=self.handle_communication)
        self.app_running = True
        self.connected = False
        self.game_running = False
        self.role = None
        self.username = None

    def _test_frame(self):
        self.SELECT_WORD_FRAME.set_words(words="apple,potato,tomato")
        self.show(frame=self.SELECT_WORD_FRAME)
        pass

    def end(self):
        """
        Closes the connection with server if connected. Closes the window. Ends the program.
        :return: None
        """
        if self.connected:
            # end connection
            comm.send(connection=self.connection, message=f"-left:{self.username}")
            self.connected = False
        self.app_running = False
        self.destroy()

    def handle_communication(self):
        """
        Main thread. Handles the received messages from the server.
        :return: None
        """

        while self.app_running:
            time.sleep(RUNNING_SLEEP)     # optimize this!

            if self.connected:
                # constantly gets the messages!
                try:
                    command_key, message = comm.receive(connection=self.connection)
                except TypeError as err:
                    Logger.print(f"[TypeError]\t{err}")
                    self.app_running = False
                except ValueError as err:
                    # print(f"[ValueError]\t{err}")
                    Logger.print(f"[ValueError]\t{err}")
                except ConnectionResetError as err:
                    # TODO: TEST THIS CONNECTIONS, TRY BLOCKS AND SO ON!!!
                    # print(f"[ConnectionResetError]\t{err}")
                    Logger.print(f"[ConnectionResetError]\t{err}")
                    self.app_running = False
                else:
                    if command_key == "-chat":
                        self.commands.get_chat(message)
                    elif command_key == "-dword":
                        self.commands.get_dword(message)
                    elif command_key == "-end":
                        self.commands.get_end(message)
                    elif command_key == "-gamestat":
                        self.commands.get_gamestat(message)
                    elif command_key == "-hword":
                        self.commands.get_hword(message)
                    elif command_key == "-image":
                        self.commands.get_image(message)
                    elif command_key == "-isword":
                        self.commands.get_isword(message)
                    elif command_key == "-join":
                        self.commands.get_join(message)
                    elif command_key == "-leaderboard":
                        self.commands.get_leaderboard(message)
                    elif command_key == "-left":
                        self.commands.get_left(message)
                    elif command_key == "-result":
                        self.commands.get_result(message)
                    elif command_key == "-role":
                        self.commands.get_role(message)
                    elif command_key == "-round":
                        self.commands.get_round(message)
                    elif command_key == "-start":
                        self.commands.get_start()
                    elif command_key == "-time":
                        self.commands.get_time(message)
                    elif command_key == "-timeisup":    # useful?
                        self.commands.get_timeisup()
                    elif command_key == "-words":
                        self.commands.get_words(message)
                    else:
                        # print(f"[Command Key]\t\t{command_key}")
                        Logger.print(f"[Command Key]\t\t{command_key}")

            else:
                if self.JOIN_FRAME.join:
                    self.username = self.JOIN_FRAME.username
                    if self.on_join():
                        self.connected = True

    def on_join(self):
        """
         Connects to the server. Sends the username.
         :return: bool
         """
        try:
            self.connection.connect((self.host, self.port))
        except Exception as err:
            # print(f"[Error 179]\t{err}\nFailed to connect with the server.")
            Logger.print(f"[Error 179]\t{err}\nFailed to connect with the server.")
            self.app_running = False
            return False
        else:
            comm.send(connection=self.connection, message=f"-username:{self.username}")
            return True

    def start_thread(self):
        """
        Starts the main thread.
        :return: None
        """
        self.thread.start()


def main():
    client = Client(host=socket.gethostname(), port=PORT)
    client.start_thread()
    tk.mainloop()


if __name__ == '__main__':
    # print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__, __name__, str(__package__)))
    main()
