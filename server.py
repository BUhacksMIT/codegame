import logging
import sys
import socketserver
import queue
import time
import pickle

class langs():
    Python = 1
    Java = 2

class retcode():
    success = 1
    fail = -1

class Ship():
    def __init__(self, player, x, y):
        self.coords = (x, y)
        self.x = x
        self.y = y
        self.player = player
        self.health = 100

class Grid():
    def __init__(self, width, height):
        self.game_width = width
        self.game_height = height
        self.ships = [Ship(1337, 10, 10)]
        self.grid = [[0 for x in range(self.game_width)] for x in range(self.game_height)]

    def is_empty(self, x, y):
        if (self.grid[x][y] == 0):
            return True
        else:
            return False

    def place_ship(self, ship):
        self.ships.append(ship)
        self.grid[ship.x][ship.y] = ship

playerqueues = {}
playerlangs = {}

def ReturnToPlayer(playerid, retval):
    p = playerqueues[playerid]
    p.put(retval)

grid = Grid(20, 40)

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

q = queue.Queue()

class EchoRequestHandler(socketserver.BaseRequestHandler):
    
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('EchoRequestHandler')
        self.logger.debug('__init__')
        self.playerid = client_address[1]
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return socketserver.BaseRequestHandler.setup(self)

    def handle(self):
        self.logger.debug('handle')

        # Echo the back to the client
        while (1==1):
            data = self.request.recv(1024)
            #self.logger.debug('recv()->"%s"', data)
            q.put((self.playerid, data))
            time.sleep(1)
            pqueue = playerqueues[self.playerid]
            while (pqueue.empty() == True):
                pass
            if (pqueue.empty() == False):
                (rcode, rval) = pqueue.get()
                if (playerlangs[self.playerid] == langs.Python):
                    r = pickle.dumps((rcode, rval))
                    self.request.send(r)
                elif (playerlangs[self.playerid] == langs.Java):
                    #self.request.send(bytes(str(r), "UTF-8"))
                    pass
            time.sleep(1)
        return

    def finish(self):
        self.logger.debug('finish')
        return socketserver.BaseRequestHandler.finish(self)

class EchoServer(socketserver.TCPServer):
    
    def __init__(self, server_address, handler_class=EchoRequestHandler):
        self.logger = logging.getLogger('EchoServer')
        self.logger.debug('__init__')
        socketserver.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        self.logger.debug('server_activate')
        socketserver.TCPServer.server_activate(self)
        return

    def serve_forever(self):
        self.logger.debug('waiting for request')
        self.logger.info('Handling requests, press <Ctrl-C> to quit')
        while True:
            self.handle_request()
        return

    def handle_request(self):
        self.logger.debug('handle_request')
        return socketserver.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)', request, client_address)
        playerqueues[client_address[1]] = queue.Queue()
        return socketserver.TCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        self.logger.debug('process_request(%s, %s)', request, client_address)
        return socketserver.TCPServer.process_request(self, request, client_address)

    def server_close(self):
        self.logger.debug('server_close')
        return socketserver.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)', request, client_address)
        return socketserver.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        self.logger.debug('close_request(%s)', request_address)
        return socketserver.TCPServer.close_request(self, request_address)

if __name__ == '__main__':
    import socket
    import threading

    address = ('localhost', 1337) # let the kernel give us a port
    server = EchoServer(address, EchoRequestHandler)
    ip, port = server.server_address # find out what port we were given

    address2 = ('localhost', 1338) # let the kernel give us a port
    server2 = EchoServer(address2, EchoRequestHandler)
    

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True) # don't hang on exit
    t.start()

    t2 = threading.Thread(target=server2.serve_forever)
    t2.setDaemon(True) # don't hang on exit
    t2.start()


    logger = logging.getLogger('client')
    logger.info('Server on %s:%s', ip, port)

    while (True):
        if (q.empty() == False):
                print ("got msg")
                (playerid, msg) = q.get()
                args = msg.decode("UTF-8").split(",")
                opcode = int(args[0])
                if (opcode == 1):
                    x = int(args[1])
                    y = int(args[2])
                    if (grid.is_empty(x, y)):
                        print("adding to grid")
                        newship = Ship(playerid, x, y)
                        grid.place_ship(newship)
                        pdata = (retcode.success, None)
                        ReturnToPlayer(playerid, pdata)
                    else:
                        pdata = (retcode.fail, None)
                        ReturnToPlayer(playerid, pdata)
                elif (opcode == 2):
                    ships = []
                    for ship in grid.ships:
                        if ship.player != playerid:
                            ships.append(ship)
                    pdata = (retcode.success, ships)
                    ReturnToPlayer(playerid, pdata)
                elif (opcode == 3):
                    print ("got language of ", str(args[1]), " for player ", str(playerid))
                    langcode = int(args[1])
                    playerlangs[playerid] = langcode
                    ReturnToPlayer(playerid, (retcode.success, None))
                else:
                    pass