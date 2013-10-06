from client import Client
from client import resultcodes
from client import Directions

gameclient = Client("localhost", 1338)

gameclient.ConnectToGame()

myships = []
mycoords = []

for i in range(gameclient.max_ships):
    rescode, resval = Initialize_Ship(i, 5)
    if (rescode == resultcodes.success):
        mycoords.append((3+i, 6+i*4))
        myships.append(resval)

k=0
i=0
while (True):
    rescode, resval = gameclient.GetDelay()
    if (resval > 0):
        print("I can't move for another ", str(resval), " ticks!")
    else:
        if (k % 2 == 0):
            rescode, resval = gameclient.Fire(myships[i], myships[i][0]+2, myships[i][1]+4)
        else:
            rescode, resval = gameclient.Move(myships[i], Directions.right)
    k = k + 1
    i= (i+ 1) % gameclient.max_ships

s.close()

