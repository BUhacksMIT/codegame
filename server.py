import logging
import sys
import socketserver
import queue
import time
import pickle
import struct
import random
import math
max_game_cmd_len = 100

class fileOpcodes():
    instantiate = 1
    move = 2
    fire = 3
    kill = 4
    endgame = 5
    eliminated = 6
    #loc = (x,y)
    #newLoc = (x,y)

interfacequeues = {}

def AddInterfaceQueueMsg(msg):
    for k in list(interfacequeues.keys()):
        interfacequeues[k].put(msg)
    return True

class fileWriter():
    def __init__(self):
       self.logFile = open('log.txt','w')
       self.numwrites = 0
    
    #Each line represents a command    
    def writeLog(self,playerID,opCode,loc=(-1,-1), newLoc = (-1,-1), **kwargs):
        self.numwrites += 1
        #create ship
        print("writing to file opcode", opCode)
        if opCode == fileOpcodes.instantiate:
            # "playerID opCode (x,y)" where (x,y) is a location on the grid
            print(fileOpcodes.instantiate, playerID, loc, file=self.logFile, end="\r\n", sep=";")
            AddInterfaceQueueMsg(str(fileOpcodes.instantiate) + ";" + str(playerID) + ";" + str(loc))
        #Move ship from loc to newLoc
        elif opCode == fileOpcodes.move:
            # "playerID opcode (x,y) (a,b)" where (x,y) and (a,b) are locations on the grid
            print(fileOpcodes.move,playerID,loc,newLoc,file = self.logFile,end="\r\n",sep=";")
            AddInterfaceQueueMsg(str(fileOpcodes.move) + ";" + str(playerID) + ";" + str(loc) + ";" + str(newLoc))
        #Fire from loc to newLoc
        elif opCode == fileOpcodes.fire:
            # "playerID opcode (x,y) (a,b)" where (x,y) and (a,b) are locations on the grid
            print(fileOpcodes.fire,playerID,loc,newLoc,file = self.logFile,end="\r\n",sep=";")
            AddInterfaceQueueMsg(str(fileOpcodes.fire) + ";" + str(playerID) + ";" + str(loc) + ";" + str(newLoc))
        #Remove a ship from the grid
        elif opCode == fileOpcodes.kill:
            # "playerID opCode (x,y)" where (x,y) is a location on the grid
            print(fileOpcodes.kill,playerID,loc,file = self.logFile,end="\r\n",sep=";")
            AddInterfaceQueueMsg(str(fileOpcodes.kill) + ";" + str(playerID) + ";" + str(loc))
        #end the game, playerID wins
        elif opCode == fileOpcodes.endgame:
            self.logFile.write(str(fileOpcodes.endgame)+";"+str(playerID)+"\r\n")
            AddInterfaceQueueMsg(str(fileOpcodes.endgame) + ";" + str(playerID))
            self.logFile.close()
        elif opCode == fileOpcodes.eliminated:
            print(fileOpcodes.eliminated,playerID, file=self.logFile, end="\r\n", sep=";")
            AddInterfaceQueueMsg(str(fileOpcodes.eliminated) + ";" + str(playerID))

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
        print("delay added!!", str(amt))
        return True

    def GetFileID(playerid): #static method
        return Player.playerfileids[playerid]

def AddPlayerDelay(playerid, delayamt):
    players[playerid].AddDelay(delayamt)
    print("adding ", str(delayamt), " to player ", str(playerid))
    print("NEW DELAY:", str(players[playerid].delay))
    return True

def EndGame():
    print("Game over. Winner:", Player.GetFileID(game.GetWinner()))
    writer.writeLog(Player.GetFileID(game.GetWinner()),fileOpcodes.endgame)
    return True

max_ships = 8
max_range = 8
max_ticks_to_add_ships = 200

def StartGame():
    game.started = True
    return True

def KillPlayer(playerid):
    print("KILL!!!!!", str(playerid))
    if (playerid in players):
        writer.writeLog(Player.GetFileID(playerid),fileOpcodes.eliminated)
        del(players[playerid])
        for ship in list(grid.ships.values()):
            if (ship.player == playerid):
                ship.alive = False
                grid.grid[ship.y][ship.x] = 0
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
            shipcount[ship.player] = shipcount.setdefault(ship.player, 0) + 1
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
            return 5
        elif (opcode == Opcodes.get_player_coords):
            return 0
        elif (opcode == Opcodes.choose_lang):
            return 0
        elif (opcode == Opcodes.move):
            return 5
        elif(opcode == Opcodes.get_delay):
            return 0
        elif (opcode == Opcodes.fire):
            return 5
        elif (opcode == Opcodes.get_my_alive_ships):
            return 0
        elif (opcode == Opcodes.get_game_status):
            return 0
class Grid():
    def __init__(self, width, height):
        self.game_width = width
        self.game_height = height
        self.ships = {}
        self.playershipcount = {}
        self.grid = [[0 for x in range(self.game_width)] for x in range(self.game_height)]

    def is_empty(self, x, y):
        if (self.grid[y][x] == 0):
            return True
        else:
            return False

    def GetShipCount(self, playerid):
        return self.playershipcount.setdefault(playerid, 0)
    def place_ship(self, ship):
        self.ships[(ship.player, ship.shipid)] = ship
        self.grid[ship.y][ship.x] = ship

    def GetShipById(self, playerid, shipid):
        return self.ships[(playerid, shipid)]

    def MoveShip(self, playerid, shipid, newx, newy):
        if (self.ships[(playerid, shipid)].alive == False):
            return retcode.shipdead
        if (newx >= grid.game_width or newx < 0 or newy >= grid.game_height or newy < 0):
            return retcode.outofbounds
        elif (self.is_empty(newx, newy)):
            shiptomove = self.GetShipById(playerid, shipid)
            oldx = shiptomove.x
            oldy = shiptomove.y
            self.grid[newy][newx] = self.grid[oldy][oldx]
            self.grid[oldy][oldx] = 0
            stu = self.ships[(shiptomove.player, shiptomove.shipid)]
            stu.x = newx
            stu.y = newy
            stu.coords = (newx, newy)
            shiptomove.x = newx
            shiptomove.y = newy
            shiptomove.coords = (newx, newy)
            return retcode.success
        else:
            return retcode.alreadyoccupied

    def ProcessFire(self, playerid, shipid, to_x, to_y):
        print ("processing fire")
        if (to_x >= self.game_width or to_y >= self.game_height or to_x < 0 or to_y < 0):
            return ((retcode.outofbounds, (self.game_width, self.game_height)))
        if (self.grid[to_y][to_x] != 0):
            killed = self.grid[to_y][to_x]
            writer.writeLog(Player.GetFileID(killed.player),fileOpcodes.kill,(killed.x,killed.y))
            ret = ((retcode.hit, (killed.player, killed.shipid)))
            self.grid[to_y][to_x] = 0
            self.ships[(killed.player, killed.shipid)].alive = False
            shipcount = {}
            for ship in list(self.ships.values()):
                if (ship.alive == True):
                    shipcount[ship.player] = shipcount.setdefault(ship.player, 0) + 1
                    print("ship count for ", str(ship.player), " updated to ", str(shipcount[ship.player]))
            for player in list(players.keys()):
                if (player not in shipcount):
                    print("killing ", str(player), " for no ships")
                    KillPlayer(player)
            return (retcode.success, killed.player)
        else:
            return (retcode.miss, None)

grid = Grid(20, 20)

class Ship():
    def __init__(self, player, x, y):
        self.coords = [x, y]
        self.x = x
        self.y = y
        self.alive = True
        self.shipid = grid.GetShipCount(player) + 1
        grid.playershipcount[player] += 1
        print("player ", player, " shipid ", self.shipid)
        self.player = player
        self.health = 100

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
    PHP = 2
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
    shipsuccess = 3 #for system use
    shipdead = -7




def ReturnToPlayer(playerid, retval):
    print ("rv:", str(retval))
    p = players[playerid].sendqueue
    p.put(retval)



logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )
class InterfaceRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('EchoRequestHandler')
        print("init conn")
        self.logger.debug('__init__')
        self.playerid = client_address[1]
        request.settimeout(0)
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return socketserver.BaseRequestHandler.setup(self)

    def handle(self):
        self.logger.debug('handle')
        data =  self.request.recv(1024, socket.MSG_PEEK)
        #args = data.decode("UTF-8").split(";")
        q = interfacequeues[self.playerid]
        while (1==1):
            if (q.empty() == False):
                msg = q.get()
                print("SENDING:::::::::::::::::::", msg)
                self.request.send(bytes(msg, "UTF-8"))
                print(msg)


    def finish(self):
        self.logger.debug('finish')
        return socketserver.BaseRequestHandler.finish(self)

class EchoRequestHandler(socketserver.BaseRequestHandler):
    
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('EchoRequestHandler')
        self.logger.debug('__init__')
        self.playerid = client_address[1]
        request.settimeout(3.0)
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
                if(self.playerid not in players):
                    print("NOT IN!!")
                    return
                data =  self.request.recv(1024, socket.MSG_PEEK)
                args = data.decode("UTF-8").split(";")
                opcode = int(args[0])
                if (opcode != Opcodes.get_delay and opcode != Opcodes.get_game_status and opcode != Opcodes.get_my_alive_ships):
                    print("delaying")
                    while (players[self.playerid].delay > 0):
                        print ("delay tick")
                        time.sleep(0.1)
                        pass
                print("continuing",opcode)
                data = self.request.recv(1024)
                print("continued")
                #self.logger.debug('recv()->"%s"', data)
                q = players[self.playerid].recvqueue
                print("data put:", str(data))
                q.put((self.playerid, data))
                #time.sleep(1)

                pqueue = players[self.playerid].sendqueue
                print("queue: ", str(pqueue), " for ", str(self.playerid))
                while (pqueue.empty() == True):
                    time.sleep(0.1)
                    pass
                if (pqueue.empty() == False):
                    pqg = pqueue.get()
                    print("pqg:", str(pqg))
                    (rcode, rval) = pqg
                    if (players[self.playerid].lang == langs.Python):
                        if (rcode == retcode.shipsuccess):
                            rcode = retcode.success
                            sl = []
                            for t in rval:
                                pid, sid = t
                                sl.append(grid.ships[(pid, sid)])
                            rval = sl
                        r = pickle.dumps((rcode, rval))
                        self.request.send(r)
                    elif (players[self.playerid].lang == langs.PHP):
                        if (rcode == retcode.shipsuccess):
                            print("special fun", str(rval))
                            rcode = retcode.success
                            sl = []
                            for t in rval:
                                pid, sid = t
                                #x, y, alive, shipid, player, health
                                ps = grid.ships[(pid, sid)]
                                sl.append((ps.x, ps.y, ps.alive, ps.shipid, ps.player, ps.health))
                            rval = sl
                        resp = str(rcode) + ";" + str(rval)
   
                        bytex = bytes(resp, "UTF-8")
                        print(struct.pack("!i", len(bytex)))
                        bytex = struct.pack("!i", len(bytex))+bytex

                        print("to php:", bytex.decode("UTF-8"))
                        self.request.send(bytex)
                        pass
            except Exception as err:
                KillPlayer(self.playerid)
                print ("Player with id ", str(self.playerid), " disconnected unexpectedly! + ", err)
                return
            time.sleep(0)
        return

    def finish(self):
        self.logger.debug('finish')
        return socketserver.BaseRequestHandler.finish(self)

class EchoServer(socketserver.TCPServer):
    
    def __init__(self, server_address, handler_class=EchoRequestHandler, interface=False):
        self.logger = logging.getLogger('EchoServer')
        self.logger.debug('__init__')
        self.interface = interface
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
        if (self.interface == False):
            if (game.started == True):
                request.close()
                return False
            print("ADD PLAYER");
            players[client_address[1]] = Player()
            game.playercount += 1
            Player.playerfileids[client_address[1]] = game.playercount
        else:
            interfacequeues[client_address[1]] = queue.LifoQueue()
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

    address2 = ('localhost', 1339) # let the kernel give us a port
    server2 = EchoServer(address2, EchoRequestHandler)
	
    address3 = ('localhost', 1341)
    server3 = EchoServer(address3, InterfaceRequestHandler, True)


    address4 = ('localhost', 1342) # let the kernel give us a port
    server4 = EchoServer(address4, InterfaceRequestHandler, True)
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True) # don't hang on exit
    t.start()

    t2 = threading.Thread(target=server2.serve_forever)
    t2.setDaemon(True) # don't hang on exit
    t2.start()

    t3 = threading.Thread(target=server3.serve_forever)
    t3.setDaemon(True) # don't hang on exit
    t3.start()

    t4 = threading.Thread(target=server4.serve_forever)
    t4.setDaemon(True) # don't hang on exit
    t4.start()
    logger = logging.getLogger('client')
    logger.info('Server on %s:%s', ip, port)

    while (True):
        if (writer.numwrites > max_game_cmd_len):
            EndGame()
            break
        if (len(players) >= players_to_start and game.started == False):
            StartGame()
        if (len(players) < 2 and game.started == True):
            EndGame()
            break
        rs = list(players.items())
        if (len(rs) > 0):
            pass
            #random.shuffle(rs)
        else:
            continue
        for k, q in rs:
            q = q.recvqueue
            loopdone = False
            while(loopdone == False):
                loopdone = True
                print("loop for ", str(k))
                if (q.empty() == False):
                        try:
                            (playerid, msg) = q.get()
                            args = msg.decode("UTF-8").split(";")
                            opcode = int(args[0])
                            print("msg of opcode ", opcode, " from ", playerid)
                            print("data:", str(args[1]))
                            if (opcode == Opcodes.initialize_ship):
                                x = int(args[1])
                                y = int(args[2])
                                print("init ship entered",x,",",y)
                                if (x < 0 or y < 0 or x >= grid.game_width or y >= grid.game_height):
                                    print("out of bounds on ship add")
                                    ReturnToPlayer(playerid, (retcode.outofbounds, (grid.game_width, grid.game_height)))
                                    AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.initialize_ship))
                                    continue
                                if ((Player.GetFileID(playerid) == 1 and y > grid.game_height / 2) or (Player.GetFileID(playerid) == 2 and y < grid.game_height / 2)):
                                    print("out of bounds on ship add")
                                    ReturnToPlayer(playerid, (retcode.outofbounds, (grid.game_width, grid.game_height)))
                                    AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.initialize_ship))
                                    continue                                                          
                                if (grid.GetShipCount(playerid) >= max_ships):
                                    print("out of ships")
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
                                    print("failed to add ship")
                                    pdata = (retcode.fail, None)
                                    ReturnToPlayer(playerid, pdata)
                                    AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.initialize_ship))
                                print("init ship exited")
                            elif (opcode == Opcodes.get_player_coords):
                                ships = []
                                for ship in list(grid.ships.values()):
                                    if (ship.player != playerid and ship.alive == True):
                                        ships.append((ship.player, ship.shipid))
                                pdata = (retcode.shipsuccess, ships)
                                ReturnToPlayer(playerid, pdata)
                                AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.get_player_coords))
                                loopdone = False
                                time.sleep(0.1)
                            elif (opcode == Opcodes.choose_lang):
                                print ("got language of ", str(args[1]), " for player ", str(playerid))
                                langcode = int(args[1])
                                players[playerid].lang = langcode
                                ReturnToPlayer(playerid, (retcode.success, None))
                                AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.choose_lang))
                            elif (opcode == Opcodes.move):
                                shipids = list(map(int, args[1].split(',')))
                                movedirs = list(map(int, args[2].split(',')))
                                rets = []
                                codes = []
                                for shipid, movedir in zip(shipids, movedirs):
                                    print("moving ", str(shipid), " in dir ", str(movedir))
                                    playership = grid.GetShipById(playerid, shipid)
                                    oldx = playership.x
                                    oldy = playership.y
                                    newx = playership.x
                                    newy = playership.y
                                    if (movedir == Directions.right or movedir == Directions.up_right or movedir == Directions.down_right):
                                        newx += 1
                                    if (movedir == Directions.left or movedir == Directions.up_left or movedir == Directions.down_left):
                                        newx -= 1
                                    if (movedir == Directions.up or movedir == Directions.up_left or movedir == Directions.up_right):
                                        newy += 1
                                    if (movedir == Directions.down or movedir == Directions.down_left or movedir == Directions.down_right):
                                        newy -= 1
                                    moveret = grid.MoveShip(playerid, shipid, newx, newy)
                                    if (moveret == retcode.success):
                                        writer.writeLog(Player.GetFileID(playerid),fileOpcodes.move,(oldx, oldy),newLoc = (newx,newy))
                                        rets.append((newx, newy, shipid, retcode.success))
                                        codes.append(retcode.success)
                                        continue
                                    elif (moveret == retcode.outofbounds):
                                        rets.append((grid.game_width, grid.game_height, shipid, moveret))
                                        codes.append(moveret)
                                        continue
                                    else:
                                        rets.append((playership.x, playership.y, shipid, moveret))
                                        codes.append(moveret)
                                        continue
                                if (len(rets) == 1):
                                    print("rl:", rets[0])
                                    ReturnToPlayer(playerid, (codes[0], rets[0]))
                                else:
                                    print("HERE:", str((codes, rets)))
                                    ReturnToPlayer(playerid, (retcode.success, rets))
                                AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.move) * len(shipids))
                            elif (opcode == Opcodes.get_delay):
                                print("sending delay of ", str(players[playerid].delay))
                                ReturnToPlayer(playerid, (retcode.success, players[playerid].delay))
                                print("delay sent")
                                AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.get_delay))
                                if (players[playerid].delay < 1):
                                    loopdone = False
                                    time.sleep(0.1)
                            elif (opcode == Opcodes.fire):
                                shipid = int(args[1])
                                to_x = int(args[2])
                                to_y = int(args[3])
                                playership = grid.GetShipById(playerid, shipid)
                                print("fire entered")
                                if (playership.alive == False):
                                    ReturnToPlayer(playerid, (retcode.shipdead, None))
                                    AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.fire))
                                    continue
                                if (to_x < 0 or to_y < 0 or to_x >= grid.game_width or to_y >= grid.game_height):
                                    print("out of bounds on ship shot")
                                    ReturnToPlayer(playerid, (retcode.outofbounds, None))
                                    AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.fire))
                                    continue
                                if (math.sqrt(abs(to_x - playership.x)**2 + abs(to_y - playership.y)**2) < max_range):
                                    print("case 1")
                                    writer.writeLog(Player.GetFileID(playerid),fileOpcodes.fire,(playership.x,playership.y),newLoc = (to_x,to_y))
                                    print("case 1 again ", to_x, " ", to_y, " ", shipid)
                                    ReturnToPlayer(playerid, grid.ProcessFire(playerid, shipid, to_x, to_y))
                                    AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.fire))
                                else:
                                    print("case 2")
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
                                loopdone = False
                                print("alive ships returned, giving another shot...")
                                time.sleep(0.1)
                            elif (opcode == Opcodes.get_game_status):
                                print("got game status request")
                                ReturnToPlayer(playerid, (retcode.success, (game.started, grid.game_width, grid.game_height, max_range, max_ships)))
                                AddPlayerDelay(playerid, Opcodes.GetDelay(Opcodes.get_game_status)) 
                                #no delay, ever
                            else:
                                print("invalid opcode", str(opcode))
                                pass
                        except:
                            pass
        TickClock()
        time.sleep(0.1)