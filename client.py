import socket
import sys
import time
import pickle

class resultcodes():
    success = 1
    hit = 2
    fail = -1
    toomanyships = -2
    alreadyoccupied = -3
    outofbounds = -4
    outofrange = -5
    miss = -6

class fileOpcodes():
    instantiate = 1
    move = 2
    fire = 3
    kill = 4
    endgame = 5
    eliminated = 6

class Opcodes():
    initialize_ship = 1
    get_player_coords = 2
    choose_lang = 3
    move = 4
    get_delay = 5
    fire = 6
    get_my_alive_ships = 7
    get_game_status = 8

class langs():
    Python = 1
    Java = 2

class Directions():
    up = 1
    up_right = 2
    right = 3
    down_right = 4
    down = 5
    down_left = 6
    left = 7
    up_left = 8

class Ship():
    def __init__(self, player, x, y):
        self.coords = (x, y)
        self.x = x
        self.y = y
        self.player = player
        self.health = 100

class Client():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.game_started = False

    def _SendCommand(opcode, *args):
        message = str(opcode) + ","
        for arg in args:
            message += str(arg) + ","
        print("sending command: " + message)
        s.send(bytes(str(message), "UTF-8"))
        response = self.s.recv(4096)
        print(response)
        return response

    def InitializeShip(x, y):
        print("init ship")
        return pickle.loads(self._SendCommand(Opcodes.initialize_ship, x, y))

    def GetPlayerCoords():
        response = self._SendCommand(Opcodes.get_player_coords)
        print("res:",response)
        response = pickle.loads(response)
        print("res2",response)
        return response

    def Move(shipid, direction):
        return pickle.loads(self._SendCommand(Opcodes.move, shipid, direction))

    def GetMyDelay():
        return pickle.loads(self._SendCommand(Opcodes.get_delay))

    def Fire(shipid, to_x, to_y):
        return pickle.loads(self._SendCommand(Opcodes.fire, shipid, to_x, to_y))

    def GetMyAliveShips():
        return pickle.loads(self._SendCommand(Opcodes.get_my_alive_ships))

    def _GetGameStatus():
        return pickle.loads(self._SendCommand(Opcodes.get_game_status))

    def ConnectToGame(host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.ip, self.port))
        self._SendCommand(Opcodes.choose_lang, langs.Python)
        while (self.game_started == False):
            rescode, resval = self._GetGameStatus()
            if (resval[0] == True):
                self.board_width = int(resval[1])
                self.board_height = int(resval[2])
                self.max_range = int(resval[3])
                self.max_ships = int(resval[4])
                self.game_started = True
                print("Game started!")
        return True
    
    def __del__(self):
        self.s.close()