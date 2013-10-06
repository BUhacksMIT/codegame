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

offset = 3
for i in range(gameclient.max_ships):
    y = random.choice([2, 3, 4, 5, 6])
    rescode, resval = gameclient.InitializeShip(3+i-offset, y)
    if (rescode == resultcodes.success):
        mycoords.append((3+i-offset, y))
        myships.append(resval)
        print ("ship success")
    else:
        print ("ship fail. try again...")
        offset += 1

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
            rescode, resval = gameclient.Fire(myships[i % len(myships)], mycoords[i % len(mycoords)][0]+2, mycoords[i % len(mycoords)][1]+4)
            print("fire  ", i, " to ",  mycoords[i % len(mycoords)][0]+random.choice([-1, 1])*random.randint(1, 5), ",", mycoords[i % len(mycoords)][1]+random.choice([-1, 1])*random.randint(1, 5), " with result ", rescode, " and value ", resval)
        else:
            rescode, resval = gameclient.Move(myships[i % len(myships)], random.randint(1,8))
            print("move  ", i, " to right with result ", rescode, " and value ", resval)
    k = k + 1
    i= (i+ 1)
    time.sleep(0.1)

s.close()

