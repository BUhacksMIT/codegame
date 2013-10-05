import opCodes

class fileWriter:
    
    logFile = open('log.txt','w')
    
    def deconstruct(self):
        self.logFile.close()

    #Each line represents a command    
    def writeLog(self,playerID,opCode,loc, newLoc = (-1,-1), **kwargs):
        #create ship
        if opCode == opCodes.instantiate:
            # "playerID opCode (x,y)" where (x,y) is a location on the grid
            print(opCodes.instantiate,playerID,loc,file = self.logFile,end="\r\n")
        #Move ship from loc to newLoc
        elif opCode == opCodes.move:
            # "playerID opcode (x,y) (a,b)" where (x,y) and (a,b) are locations on the grid
            print(opCodes.move,playerID,loc,newLoc,file = self.logFile,end="\r\n")
        #Fire from loc to newLoc
        elif opCode == opCodes.fire:
            # "playerID opcode (x,y) (a,b)" where (x,y) and (a,b) are locations on the grid
            print(opCodes.fire,playerID,loc,newLoc,file = self.logFile,end="\r\n")
        #Remove a ship from the grid
        elif opCode == opCodes.kill:
            # "playerID opCode (x,y)" where (x,y) is a location on the grid
            print(opCodes.kill,playerID,loc,file = self.logFile,end="\r\n")