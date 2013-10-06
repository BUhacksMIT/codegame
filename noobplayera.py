from client import Client
from client import resultcodes
from client import Directions
import random
import time

random.seed()

gameclient = Client("localhost", 1339)

gameclient.ConnectToGame()

myships = []
mycoords = []

for i in range(gameclient.max_ships-1):
    rescode, resval = gameclient.InitializeShip(5+i, 10+i*4)
    if (rescode == resultcodes.success):
        mycoords.append((5+i, 10+i*4))
        myships.append(resval)
        print ("ship success")
    else:
        print ("ship fail")

k=0
i=0
while (True):
    print("getting delay")
    rescode, resval = gameclient.GetMyDelay()
    print("delay is ", resval, " with code ", rescode)
    if (resval > 0):
        print("I can't move for another ", str(resval), " ticks!")
    else:
        if (k % 2 == 0):
            rescode, resval = gameclient.Fire(myships[i], mycoords[i][0]+2, mycoords[i][1]+4)
            print("fire  ", i, " to ",  mycoords[i][0]+random.choice([-1, 1])*random.randint(1, 5), ",", mycoords[i][1]+random.choice([-1, 1])*random.randint(1, 5), " with result ", rescode, " and value ", resval)
        else:
            rescode, resval = gameclient.Move(myships[i], random.randint(1,8))
            print("move  ", i, " to right with result ", rescode, " and value ", resval)
    k = k + 1
    i= (i+ 1) % (gameclient.max_ships-1)
    time.sleep(0.1)

s.close()

