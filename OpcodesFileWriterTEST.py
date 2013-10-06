import fileWriter as fw
class fileOpcodes():
    instantiate = 1
    move = 2
    fire = 3
    kill = 4
    endgame = 5
    eliminated = 6

writer = fw.fileWriter()
writer.writeLog(1,fileOpcodes.instantiate,(2,3))
writer.writeLog(2,fileOpcodes.move,(2,3),newLoc = (4,3))
writer.writeLog(1,fileOpcodes.fire,(2,3),newLoc = (4,3))
writer.writeLog(2,fileOpcodes.kill,(2,5))
writer.deconstruct()