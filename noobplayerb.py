from client import Client
from client import resultcodes
from client import Directions
from client import Ship
import random
import time
import math

print("Player B initialize!")
print("Seeding the random number generator")
random.seed()
print("Connecting to server johnamoore.com...")
gameclient = Client("johnamoore.com", 1339)
print("Joining game...")
gameclient.ConnectToGame()
print("Game joined! Adding ships:")
mycoords = {}


offset = [0, 0]
for i in range(gameclient.max_ships):
    y = random.choice(range(11, 19)) + offset[1]
    x = i*2+random.randint(1,5)+ offset[0]
    rescode, resval = gameclient.InitializeShip(x,y)
    print("Attempting to initialize ship at ", str(x), ",", str(y))
    if (rescode == resultcodes.success):
        mycoords[resval] = [x,y]
        print("Ship successfully placed")
    else:
        print("Ship placement failed! Trying again with an offset...")
        offset = [random.randint(-3, 3), random.randint(-3, 3)]
k = 0
i = 0   
while (True):
    print("Checking for delay from previous moves")
    rescode, resval = gameclient.GetMyDelay()
    print("I have a delay of ", resval)
    if (resval > 0):
        print("I have a delay of ", str(resval), "! Waiting...")
    else:
        print("Checking to see which ships are alive")
        rescode, resval = gameclient.GetMyAliveShips()
        delcoords = []
        print("Deleting dead ships from my fleet")
        for id in mycoords:
            if id not in resval:
                delcoords.append(id)
                print("Removing my ship with id ", str(id, " since it's dead")
        for a in delcoords:
            del mycoords[a]
        print("Scouting enemy territory")
        rescode, opShips = gameclient.GetPlayerCoords()
        for ship in opShips:
            print("Enemy found! ", str(ship.coords))
        else:
            print("Finding closest enemy")
            minDistance = 40
            fireX = 0
            fireY = 0
            for ship in opShips:
                for id in mycoords:
                    dist = math.sqrt((ship.x-mycoords[id][0])**2 + (ship.y-mycoords[id][1])**2)
                    if dist < minDistance and ship.alive:
                        minDistance = dist
                        shipID = id
                        fireX = ship.x
                        fireY = ship.y
            print("Minimum distance to enemy: ",minDistance,", at coordinates ", fireX,",",fireY," (shipid=",shipID,")")
            if minDistance < 8:
                print("We're in range! Nuke 'em!")
                rescode, resval = gameclient.Fire(shipID,fireX,fireY)
                print ("Nuking them with our ship #", str(shipID))
            else:
                print("Moving toward closest enemy!")
                mdir = 1
                myship = mycoords[shipID]
                if (myship[0] < fireX and myship[1] == fireY):
                    mdir = Directions.right
                elif (myship[0] < fireX and myship[1] < fireY):
                    mdir= Directions.up_right
                elif (myship[0] < fireX and myship[1] > fireY):
                    mdir = Directions.down_right
                elif (myship[0] == fireX and myship[1] > fireY):
                    mdir = Directions.down
                elif (myship[0] == fireX and myship[1] < fireY):
                    mdir = Directions.up
                elif (myship[0] > fireX and myship[1] == fireY):
                    mdir = Directions.left
                elif (myship[0] > fireX and myship[1] < fireY):
                    mdir = Directions.up_left
                elif (myship[0] > fireX and myship[1] > fireY):
                    mdir = Directions.down_left
                rescode, resval = gameclient.Move(shipID,mdir)
                if rescode == resultcodes.success:
                    print("Move was a success!")
                    mycoords[shipID][1] = resval[1]
                    mycoords[shipID][0] = resval[0]
                else:
                    print("Failed to move")
        k = k + 1
    time.sleep(0.1)
                    
s.close()

