import socket
import sys
import time
import logging

class Opcodes():
    initialize_ship = 1
    get_player_coords = 2



def SendCommand(opcode):
    message = opcode + ","
    s.send(bytes(message, "UTF-8"))
    response = s.recv(4096)
    return response


def GetPlayerCoords():
    return SendCommand(Opcodes.get_player_coords)

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
while (True):
    pc = GetPlayerCoords()
    print(str(pc))
    time.sleep(1);

# Receive a response
logger.debug('waiting for response')
response = s.recv(len_sent)
logger.debug('response from server: "%s"', response)

# Clean up
logger.debug('closing socket')
s.close()
logger.debug('done')

