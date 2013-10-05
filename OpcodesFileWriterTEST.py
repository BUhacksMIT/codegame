import fileWriter as fw
from opcodes import opCodes

writer = fw.fileWriter()
writer.writeLog(1,opCodes.instantiate,(2,3))
writer.writeLog(2,opCodes.move,(2,3),newLoc = (4,3))
writer.writeLog(1,opCodes.fire,(2,3),newLoc = (4,3))
writer.writeLog(2,opCodes.kill,(2,4))
writer.deconstruct()