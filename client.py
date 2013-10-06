import socket
import sys
import time
import logging
import pickle

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

def SendCommand(opcode, *args):
    message = str(opcode) + ","
    for arg in args:
        message += str(arg) + ","
    print("sending command: " + message)
    s.send(bytes(str(message), "UTF-8"))
    response = s.recv(4096)
    print(response)
    return response

def Initialize_Ship(x, y):
    print("init ship")
    return pickle.loads(SendCommand(1, x, y))

def GetPlayerCoords():
    response = SendCommand(Opcodes.get_player_coords)
    print("res:",response)
    response = pickle.loads(response)
    print("res2",response)
    return response

def Move(shipid, direction):
    return pickle.loads(SendCommand(Opcodes.move, shipid, direction))

def GetDelay():
    return pickle.loads(SendCommand(Opcodes.get_delay))
def Fire(shipid, to_x, to_y):
    return pickle.loads(SendCommand(Opcodes.fire, shipid, to_x, to_y))

def GetMyAliveShips():
    return pickle.loads(SendCommand(Opcodes.get_my_alive_ships))

def GetGameStatus():
    return pickle.loads(SendCommand(Opcodes.get_game_status))

ip, port = "localhost", 1337


logger = logging.getLogger('client')
logger.info('client on %s:%s', ip, port)

# Connect to the server
logger.debug('creating socket')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logger.debug('connecting to server')
s.connect((ip, port))

# Send the data
message = 'Hello, world yo 4'
logger.debug('sending data: "%s"', message)

SendCommand(Opcodes.choose_lang, langs.Python) # 1 is for Python
game_started = False
while (game_started == False):
    rescode, resval = GetGameStatus()
    if (resval == True):
        game_started = True
        print("Game started!")
rescode, resval = Initialize_Ship(5, 5)
print(rescode)
print(resval)
shiptomove=resval
while (True):
    rescode, resval = GetDelay()
    print(resval)
    if (resval > 0):
        print("I can't move for another ", str(resval), " ticks!")
    else:
        rescode, resval = Fire(shiptomove, 15, 15)
        print(rescode)
        print(resval)
    time.sleep(1);

# Receive a response
logger.debug('waiting for response')
response = s.recv(len_sent)
logger.debug('response from server: "%s"', response)

# Clean up
logger.debug('closing socket')
s.close()
logger.debug('done')

