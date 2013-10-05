import logging
import sys
import socketserver
import queue
import time

class retcode():
    success = 1
    fail = -1

class Ship():
    def __init__(self, x, y):
        self.coords = (x, y)
        self.x = x
        self.y = y
        self.health = 100

class Grid():
    def __init__(self, width, height):
        self.game_width = width
        self.game_height = height
        self.ships = []
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
                r = pqueue.get()
                print("sending " + str(r))
                self.request.send(bytes(str(r), "UTF-8"))
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
                        newship = Ship(x, y)
                        grid.place_ship(newship)
                        ReturnToPlayer(playerid, retcode.success)
                    else:
                        ReturnToPlayer(playerid, retcode.fail)
                elif (opcode == 2):
                    pass
                else:
                    pass