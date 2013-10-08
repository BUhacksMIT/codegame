from client import Client
from client import resultcodes
from client import Directions
from client import Ship
import random
import time
import math

random.seed()

gameclient = Client("localhost", 1337)

gameclient.ConnectToGame()

mycoords = {}

offset = [0, 0]
for i in range(gameclient.max_ships):
	y = random.choice(range(1, 7)) + offset[1]
	x = i*2+random.randint(1,5)+ offset[0]
	rescode, resval = gameclient.InitializeShip(x,y)
	if (rescode == resultcodes.success):
		mycoords[resval] = [x,y]
		print("Ship successfully created")
	else:
		offset = [random.randint(-3, 3), random.randint(-3, 3)]
k = 0
i = 0	
while (True):
	rescode, resval = gameclient.GetMyDelay()
	print("delay is ", resval, " with code ", rescode)
	if (resval > 0):
		print("I can't move for another ", str(resval), " ticks!")
	else:
		rescode, resval = gameclient.GetMyAliveShips()
		delcoords = []
		for id in mycoords:
			if id not in resval:
				delcoords.append(id)
				print("Removing my ship with id ", str(id))
		for a in delcoords:
			del mycoords[a]
		for id in mycoords:
			print("HERE",mycoords[id])
		#if (k % 2 == 0):
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
						fireX = ship.x
						fireY = ship.y
			print("MinDistance",minDistance,fireX,fireY,shipID)
			if minDistance < 8:
				rescode, resval = gameclient.Fire(shipID,fireX,fireY)
				print ("firing with ship ", str(shipID))
				#print("Fire to {0}, {1}",String.Format(fireX,fireY)
			else:
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
					mycoords[shipID][1] = resval[1]
					mycoords[shipID][0] = resval[0]
		k = k + 1
	time.sleep(0.1)
					
s.close()

