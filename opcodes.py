import fileWriter as fw

class opCodes():
    instantiate = 1
    move = 2
    fire = 3
    kill = 4
    #loc = (x,y)
    #newLoc = (x,y)
            
if __name__ == "__main__":
    writer = fw.fileWriter()
    writer.writeLog(1,opCodes.instantiate,(2,3))
    writer.writeLog(2,opCodes.move,(2,3),newLoc = (4,3))
    writer.writeLog(1,opCodes.fire,(2,3),newLoc = (4,3))
    writer.writeLog(2,opCodes.kill,(2,4))
    writer.deconstruct()
    