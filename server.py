import logging
import sys
import socketserver
import queue
import time
import pickle

playerdelays = {}

def AddPlayerDelay(playerid, delayamt):
    playerdelays[playerid] += delayamt

def TickClock():
    for k in playerdelays:
        if (playerdelays[k] > 0):
            playerdelays[k] -= 1

max_ships = 5
class Opcodes():
    initialize_ship = 1
    get_player_coords = 2
    choose_lang = 3
    move = 4
    get_delay = 5

    def GetDelay(opcode): #static method
        if (opcode == Opcodes.initialize_ship):
            return 10
        elif (opcode == Opcodes.get_player_coords):
            return 10
        elif (opcode == Opcodes.choose_lang):
            return 0
        elif (opcode == Opcodes.move):
            return 10
        elif(opcode == Opcodes.get_delay):
            return 0

class Grid():
    def __init__(self, width, height):
        self.game_width = width
        self.game_height = height
        self.ships = {}
        self.playershipcount = {}
        self.grid = [[0 for x in range(self.game_width)] for x in range(self.game_height)]

    def is_empty(self, x, y):
        if (self.grid[x][y] == 0):
            return True
        else:
            return False

    def place_ship(self, ship):
        self.ships[(ship.player, ship.shipid)] = ship
        self.grid[ship.x][ship.y] = ship

    def GetShipById(self, playerid, shipid):
        return self.ships[(playerid, shipid)]

    def MoveShip(self, playerid, shipid, newx, newy):
        if (self.is_empty(newx, newy)):
            shiptomove = self.GetShipById(playerid, shipid)
            oldx = shiptomove.x
            oldy = shiptomove.y
            self.grid[newx][newy] = self.grid[oldx][oldy]
            self.grid[oldx][oldy] = 0
            shiptomove.x = newx
            shiptomove.y = newy

        else:
            return False

grid = Grid(20, 40)

class Directions():
    up = 1
    up_right = 2
    right = 3
    down_right = 4
    down = 5
    down_left = 6
    left = 7
    up_left = 8

class langs():
    Python = 1
    Java = 2

class retcode():
    success = 1
    fail = -1
    toomanyships = -2
    alreadyoccupied = -3

class Ship():
    def __init__(self, player, x, y):
        self.coords = (x, y)
        self.x = x
        self.y = y
        self.shipid = grid.playershipcount[player] + 1
        self.player = player
        self.health = 100




playersendqueues = {}
playerrecvqueues = {}
playerlangs = {}

def ReturnToPlayer(playerid, retval):
    p = playersendqueues[playerid]
    p.put(retval)



logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

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
            data =  self.request.recv(1024, socket.MSG_PEEK)
            args = data.decode("UTF-8").split(",")
            opcode = int(args[0])
            if (opcode != Opcodes.get_delay):
                while (playerdelays[self.playerid] > 0):
                    pass
            data = self.request.recv(1024)
            #self.logger.debug('recv()->"%s"', data)
            q = playerrecvqueues[self.playerid]
            q.put((self.playerid, data))
            time.sleep(1)
            pqueue = playersendqueues[self.playerid]
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
        playersendqueues[client_address[1]] = queue.Queue()
        playerrecvqueues[client_address[1]] = queue.Queue()
        grid.playershipcount[client_address[1]] = 0
        playerdelays[client_address[1]] = 0
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
        for q in list(playerrecvqueues.values()):
            if (q.empty() == False):
                    print ("got msg")
                    (playerid, msg) = q.get()
                    args = msg.decode("UTF-8").split(",")
                    opcode = int(args[0])
                    if (opcode == Opcodes.initialize_ship):
                        x = int(args[1])
                        y = int(args[2])
                        if (grid.playershipcount[playerid] >= max_ships):
                            ReturnToPlayer(playerid, (retcode.toomanyships, max_ships))
                            AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.initialize_ship))
                            continue
                        elif (grid.is_empty(x, y)):
                            print("adding to grid")
                            newship = Ship(playerid, x, y)
                            grid.place_ship(newship)
                            pdata = (retcode.success, newship.shipid)
                            ReturnToPlayer(playerid, pdata)
                            AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.initialize_ship))
                        else:
                            pdata = (retcode.fail, None)
                            ReturnToPlayer(playerid, pdata)
                            AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.initialize_ship))
                    elif (opcode == Opcodes.get_player_coords):
                        ships = []
                        for ship in grid.ships:
                            if ship.player != playerid:
                                ships.append(ship)
                        pdata = (retcode.success, ships)
                        ReturnToPlayer(playerid, pdata)
                        AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.get_player_coords))
                    elif (opcode == Opcodes.choose_lang):
                        print ("got language of ", str(args[1]), " for player ", str(playerid))
                        langcode = int(args[1])
                        playerlangs[playerid] = langcode
                        ReturnToPlayer(playerid, (retcode.success, None))
                        AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.choose_lang))
                    elif (opcode == Opcodes.move):
                        shipid = int(args[1])
                        movedir = int(args[2])
                        playership = grid.GetShipById(playerid, shipid)
                        newx = playership.x
                        newy = playership.y
                        if (movedir == Directions.right or movedir == Directions.up_right or movedir == Directions.down_right):
                            newx += 1
                        if (movedir == Directions.left or movedir == Directions.up_left or movedir == Directions.down_left):
                            newy -= 1
                        if (movedir == Directions.up or movedir == Directions.up_left or movedir == Directions.up_right):
                            newy += 1
                        if (movedir == Directions.down or movedir == Directions.down_left or movedir == Directions.down_right):
                            newy -= 1
                        if (grid.MoveShip(playerid, shipid, newx, newy)):
                            ReturnToPlayer(playerid, (retcode.success, (newx, newy)))
                            AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.move))
                            continue
                        else:
                            ReturnToPlayer(playerid, (retcode.alreadyoccupied, (playership.x, playership.y)))
                            AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.move))
                            continue
                    elif (opcode == Opcodes.get_delay):
                        print("sending delay")
                        ReturnToPlayer(playerid, (retcode.success, playerdelays[playerid]))
                        AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.get_delay))
                    else:
                        print("invalid opcode", str(opcode))
                        pass
        TickClock()
        print("tick!")
        time.sleep(1)