import logging
import sys
import socketserver
import queue
import time
import pickle

class fileOpcodes():
    instantiate = 1
    move = 2
    fire = 3
    kill = 4
    endgame = 5
    eliminated = 6
    #loc = (x,y)
    #newLoc = (x,y)

class fileWriter():
    def __init__(self):
       self.logFile = open('log.txt','w')
    
    #Each line represents a command    
    def writeLog(self,playerID,opCode,loc=(-1,-1), newLoc = (-1,-1), **kwargs):
        #create ship
        print("writing to file opcode", opCode)
        if opCode == fileOpcodes.instantiate:
            # "playerID opCode (x,y)" where (x,y) is a location on the grid
            print(fileOpcodes.instantiate, playerID, loc, file=self.logFile, end="\r\n", sep=";")
        #Move ship from loc to newLoc
        elif opCode == fileOpcodes.move:
            # "playerID opcode (x,y) (a,b)" where (x,y) and (a,b) are locations on the grid
            print(fileOpcodes.move,playerID,loc,newLoc,file = self.logFile,end="\r\n",sep=";")
        #Fire from loc to newLoc
        elif opCode == fileOpcodes.fire:
            # "playerID opcode (x,y) (a,b)" where (x,y) and (a,b) are locations on the grid
            print(fileOpcodes.fire,playerID,loc,newLoc,file = self.logFile,end="\r\n",sep=";")
        #Remove a ship from the grid
        elif opCode == fileOpcodes.kill:
            # "playerID opCode (x,y)" where (x,y) is a location on the grid
            print(fileOpcodes.kill,playerID,loc,file = self.logFile,end="\r\n",sep=";")
        #end the game, playerID wins
        elif opCode == fileOpcodes.endgame:
            self.logFile.write(str(fileOpcodes.endgame)+";"+str(playerID)+"\r\n")
            self.logFile.close()
        elif opCode == fileOpcodes.eliminated:
            print(fileOpcodes.eliminated,playerID, file=self.logFile, end="\r\n", sep=";")

players = {}

    
class Game():
    def __init__(self):
        self.started = False
        self.playercount = 0
        self.tc = 0 # tick count

    def GetWinner(self):
        shipcount = {}
        for gameship in list(grid.ships.values()):
            if (gameship.player in players):
                shipcount[gameship.player] = shipcount.setdefault(gameship.player, 0) + 1
        if (len(shipcount) == 0):
            for gameship in list(grid.ships.values()):
                shipcount[gameship.player] = shipcount.setdefault(gameship.player, 0) + 1
            return max(shipcount, key=shipcount.get)
        else:
            return max(shipcount, key=shipcount.get)


game = Game()
players_to_start = 2
writer = fileWriter()

class Player():
    playerfileids = {}

    def __init__(self):
        self.delay = 0
        self.lang = -1
        self.recvqueue = queue.Queue()
        self.sendqueue = queue.Queue()

    def AddDelay(self, amt):
        self.delay += amt

    def GetFileID(playerid): #static method
        return Player.playerfileids[playerid]

def AddPlayerDelay(playerid, delayamt):
    players[playerid].AddDelay(delayamt)
    return True

def EndGame():
    print("Game over. Winner:", Player.GetFileID(game.GetWinner()))
    writer.writeLog(Player.GetFileID(game.GetWinner()),fileOpcodes.endgame)
    return True

max_ships = 5
max_range = 5
max_ticks_to_add_ships = 100

def StartGame():
    game.started = True
    return True

def KillPlayer(playerid):
    if (playerid in players):
        writer.writeLog(Player.GetFileID(playerid),fileOpcodes.eliminated)
        del(players[playerid])
        for ship in list(grid.ships.values()):
            if (ship.player == playerid):
                ship.alive = False
                grid.grid[ship.x][ship.y] = 0
        return True
    else:
        return False

def TickClock():
    for p in list(players.values()):
        if (p.delay > 0):
            p.delay -= 1
    if (game.started == False):
        return False
    game.tc += 1
    if (game.tc > max_ticks_to_add_ships):
        shipcount = {}
        for ship in list(grid.ships.values()):
            shipcount[playerid] = shipcount.setdefault(playerid, 0) + 1
        for player in list(shipcount.keys()):
            if (shipcount[player] < max_ships):
                KillPlayer(player)
        return True

class Opcodes():
    initialize_ship = 1
    get_player_coords = 2
    choose_lang = 3
    move = 4
    get_delay = 5
    fire = 6
    get_my_alive_ships = 7
    get_game_status = 8

    def GetDelay(opcode): #static method
        if (opcode == Opcodes.initialize_ship):
            return 2
        elif (opcode == Opcodes.get_player_coords):
            return 1
        elif (opcode == Opcodes.choose_lang):
            return 0
        elif (opcode == Opcodes.move):
            return 1
        elif(opcode == Opcodes.get_delay):
            return 0
        elif (opcode == Opcodes.fire):
            return 3
        elif (opcode == Opcodes.get_my_alive_ships):
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
        if (newx >= game_width or newx < 0 or newy >= game_height or newy < 0):
            return retcode.outofbounds
        elif (self.is_empty(newx, newy)):
            shiptomove = self.GetShipById(playerid, shipid)
            oldx = shiptomove.x
            oldy = shiptomove.y
            self.grid[newx][newy] = self.grid[oldx][oldy]
            self.grid[oldx][oldy] = 0
            shiptomove.x = newx
            shiptomove.y = newy
            return retcode.success
        else:
            return retcode.alreadyoccupied

    def ProcessFire(self, playerid, shipid, to_x, to_y):
        if (to_x >= game_width or to_y >= game_height or to_x < 0 or to_y < 0):
            return ((retcode.outofbounds, (game_width, game_height)))
        if (self.grid[to_x][to_y] != 0):
            killed = self.grid[to_x][to_y]
            writer.writeLog(Player.GetFileID(killed.player),fileOpcodes.kill,(killed.x,killed.y))
            ret = ((retcode.hit, (killed.player, killed.shipid)))
            self.grid[to_x][to_y] = 0
            self.ships[(killed.player, killed.shipid)].alive = False
            return ret
        else:
            return (retcode.miss, None)

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
    NoLang = -1

class retcode():
    success = 1
    hit = 2
    fail = -1
    toomanyships = -2
    alreadyoccupied = -3
    outofbounds = -4
    outofrange = -5
    miss = -6

class Ship():
    def __init__(self, player, x, y):
        self.coords = (x, y)
        self.x = x
        self.y = y
        self.alive = True
        self.shipid = grid.playershipcount[player] + 1
        self.player = player
        self.health = 100


def ReturnToPlayer(playerid, retval):
    p = players[playerid].sendqueue
    p.put(retval)



logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

class EchoRequestHandler(socketserver.BaseRequestHandler):
    
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('EchoRequestHandler')
        self.logger.debug('__init__')
        self.playerid = client_address[1]
        request.settimeout(1.0)
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return socketserver.BaseRequestHandler.setup(self)

    def handle(self):
        self.logger.debug('handle')

        # Echo the back to the client
        while (1==1):
            try:
                data =  self.request.recv(1024, socket.MSG_PEEK)
                args = data.decode("UTF-8").split(",")
                opcode = int(args[0])
                if (opcode != Opcodes.get_delay):
                    while (players[self.playerid].delay > 0):
                        pass
                data = self.request.recv(1024)
                #self.logger.debug('recv()->"%s"', data)
                q = players[self.playerid].recvqueue
                q.put((self.playerid, data))
                time.sleep(1)
                pqueue = players[self.playerid].sendqueue
                while (pqueue.empty() == True):
                   pass
                if (pqueue.empty() == False):
                    (rcode, rval) = pqueue.get()
                    if (players[self.playerid].lang == langs.Python):
                        r = pickle.dumps((rcode, rval))
                        self.request.send(r)
                    elif (players[self.playerid].lang == langs.Java):
                        #self.request.send(bytes(str(r), "UTF-8"))
                        pass
            except:
                KillPlayer(self.playerid)
                print ("Player with id ", str(self.playerid), " disconnected unexpectedly!")
                return
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
        if (game.started == True):
            request.close()
            return False
        players[client_address[1]] = Player()
        game.playercount += 1
        Player.playerfileids[client_address[1]] = game.playercount
        grid.playershipcount[client_address[1]] = 0
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
        if (len(players) >= players_to_start and game.started == False):
            StartGame()
        if (len(players) < 2 and game.started == True):
            EndGame()
            break
        for q in list(players.values()):
            q = q.recvqueue
            if (q.empty() == False):
                    try:
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
                                writer.writeLog(Player.GetFileID(playerid),fileOpcodes.instantiate,(x,y))
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
                            players[playerid].lang = langcode
                            ReturnToPlayer(playerid, (retcode.success, None))
                            AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.choose_lang))
                        elif (opcode == Opcodes.move):
                            shipid = int(args[1])
                            movedir = int(args[2])
                            playership = grid.GetShipById(playerid, shipid)
                            oldx = playership.x
                            oldy = playership.y
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
                            moveret = grid.MoveShip(playerid, shipid, newx, newy)
                            if (moveret == retcode.success):
                                writer.writeLog(Player.GetFileID(playerid),fileOpcodes.move,(oldx, oldy),newLoc = (newx,newy))
                                ReturnToPlayer(playerid, (retcode.success, (newx, newy)))
                                AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.move))
                                continue
                            elif (moveret == retcode.outofbounds):
                                ReturnToPlayer(playerid, (moveret, (game_width, game_height)))
                                AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.move))
                                continue
                            else:
                                ReturnToPlayer(playerid, (moveret, (playership.x, playership.y)))
                                AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.move))
                                continue
                        elif (opcode == Opcodes.get_delay):
                            print("sending delay")
                            ReturnToPlayer(playerid, (retcode.success, players[playerid].delay))
                            AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.get_delay))
                        elif (opcode == Opcodes.fire):
                            shipid = int(args[1])
                            to_x = int(args[2])
                            to_y = int(args[3])
                            playership = grid.GetShipById(playerid, shipid)
                            if (abs(to_x - playership.x) < max_range and abs(to_y-playership.y) < max_range):
                                writer.writeLog(Player.GetFileID(playerid),fileOpcodes.fire,(playership.x,playership.y),newLoc = (to_x,to_y))
                                ReturnToPlayer(playerid, grid.ProcessFire(playerid, shipid, to_x, to_y))
                                AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.fire))
                            else:
                                ReturnToPlayer(playerid, (retcode.outofrange, max_range))
                                AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.fire))                            
                                continue
                        elif (opcode == Opcodes.get_my_alive_ships):
                            alive = []
                            for ship in list(grid.ships.values()):
                                if (ship.alive == True and ship.player == playerid):
                                    alive.append(ship.shipid)
                            ReturnToPlayer(playerid, (retcode.success, alive))
                            AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.get_my_alive_ships)) 
                        elif (opcode == Opcodes.get_game_status):
                            ReturnToPlayer(playerid, (retcode.success, game.started))
                            #no delay, ever
                        else:
                            print("invalid opcode", str(opcode))
                            pass
                    except:
                        pass
        TickClock()
        print("tick!")
        time.sleep(0.1)