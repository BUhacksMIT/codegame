from client import Client
from client import resultcodes
from client import Directions
from client import Ship
import random
import time
import math

random.seed()

gameclient = Client("localhost", 1339)

gameclient.ConnectToGame()

mycoords = {}

for i in range(gameclient.max_ships):
	y = random.choice([1,2,3,4,5])
	rescode, resval = gameclient.InitializeShip(i*2,y)
	if (rescode == resultcodes.success):
		mycoords[resval] = (i*2,y)
		print("Ship successfully created")
k = 0
i = 0	
while (True):
	rescode, resval = gameclient.GetMyDelay()
	print("delay is ", resval, " with code ", rescode)
	if (resval > 0):
		print("I can't move for another ", str(resval), " ticks!")
		rescode, resval = gameclient.GetMyAliveShips()
		for id in mycoords:
			if id not in resval:
				del mycoords[id]
	else:
		if (k % 2 == 0):
			rescode, opShips = gameclient.GetPlayerCoords()
			for ship in opShips:
				print(ship.coords)
		else:
			#find closest ship
			minDistance = 40
			for ship in opShips:
				for id in mycoords:
					dist = math.sqrt((ship.x-mycoords[id][0])**2 + (ship.y-mycoords[id][1])**2)
					if dist < minDistance and ship.alive:
						minDistance = dist
						shipID = id
						fireX = ship.coords[0]
						fireY = ship.coords[1]
			print("MinDistance",minDistance,fireX,fireY)
			if minDistance < 8:
				rescode, resval = gameclient.Fire(shipID,fireX,fireY)
				#print("Fire to {0}, {1}",String.Format(fireX,fireY)
			else:
				rescode, resval = gameclient.Move(shipID,1)
		k = k + 1
	time.sleep(0.1)
					
s.close()

