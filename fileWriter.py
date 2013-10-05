class fileWriter:
    
    logFile = open('log.txt','w')
    
    def deconstruct(self):
        self.logFile.close()

    #Each line represents a command    
    def writeLog(self,playerID,opCode,loc, newLoc = (-1,-1)):
        #create ship
        if opCode == 1:
            # "playerID opCode (x,y)" where (x,y) is a location on the grid
            print(playerID,1,loc,file = self.logFile)
        #Move ship from loc to newLoc
        elif opCode == 2:
            # "playerID opcode (x,y) (a,b)" where (x,y) and (a,b) are locations on the grid
            print(playerID,2,loc,newLoc,file = self.logFile)
        #Fire from loc to newLoc
        elif opCode == 3:
            # "playerID opcode (x,y) (a,b)" where (x,y) and (a,b) are locations on the grid
            print(playerID,3,loc,newLoc,file = self.logFile)
        #Remove a ship from the grid
        elif opCode == 4:
            # "playerID opCode (x,y)" where (x,y) is a location on the grid
            print(playerID,4,loc,file = self.logFile)