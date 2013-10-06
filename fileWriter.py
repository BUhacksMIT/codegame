class fileOpcodes():
    instantiate = 1
    move = 2
    fire = 3
    kill = 4
    endgame = 5
    eliminated = 6

class fileWriter:
    
    logFile = open('log.txt','w')
    
    def deconstruct(self):
        self.logFile.close()

    #Each line represents a command    
    def writeLog(self,playerID,opCode,loc=(-1,-1), newLoc = (-1,-1), **kwargs):
        #create ship
        print("writing to file")
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
            print(fileOpcodes.endgame,playerID, file=self.logFile, end="\r\n", sep=";")
        elif opCode == fileOpcodes.eliminated:
            print(fileOpcodes.eliminated,playerID)