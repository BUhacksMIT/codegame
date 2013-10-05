
using System.IO.FileInfo;
 
fileInfo= new FileInfo(fileName);

string myPath = fileInfo.DirectoryName;;
if (!System.IO.Directory.Exists(myPath))
    System.IO.Directory.CreateDirectory(myPath+@"\log");


