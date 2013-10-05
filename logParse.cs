using System;
using System.Collections;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.IO;
using System.IO.FileInfo;
using System.Text.RegularExpressions;
 
fileInfo= new FileInfo(fileName);

string log;
string myPath = fileInfo.DirectoryName;;
if (System.IO.Directory.Exists(myPath+@"\log")) {
    string log = File.ReadAllText(myPath+@"\log"+@"\log.txt");
    char newLine = "\r\n";
    string[] commands = Regex.Split(value, newLine);;
    for (int i = 0; i < commands[i].Length; i++) {
        if (commands[i][0] == "1")
        {
            //Place a new ship
            commands[i] = commands[i].Substring(2,commands[i].Length);
            string[] args = commands[i].Split(';');
            int playerID = ToInt32(args[0]);
            byte[] loc = {(byte)ToInt32(args[1][1]),(byte)ToInt32(args[1][4])};
            //Call function(playerID,loc)
        }
        else if (commands[i][0] == "2")
        {
            //Move a ship
            commands[i] = commands[i].Substring(2,commands[i].Length);
            string[] args = commands[i].Split(';');
            int playerID = ToInt32(args[0]);
            byte[] loc = {(byte)ToInt32(args[1][1]),(byte)ToInt32(args[1][4])};
            byte[] newLoc = {(byte)ToInt32(args[2][1]),(byte)ToInt32(args[2][4])};
            //Call function(playerID,loc,newLoc)
        }
        else if (commands[i][0] == "3")
        {
            //Fire at another ship
            commands[i] = commands[i].Substring(2,commands[i].Length);
            string[] args = commands[i].Split(';');
            int playerID = ToInt32(args[0]);
            byte[] loc = {(byte)ToInt32(args[1][1]),(byte)ToInt32(args[1][4])};
            byte[] newLoc = {(byte)ToInt32(args[2][1]),(byte)ToInt32(args[2][4])};
            //Call function(playerID,loc,newLoc)
        }
        else if (commands[i][0] == "4")
        {
            //Remove a ship from grid
            commands[i] = commands[i].Substring(2,commands[i].Length);
            string[] args = commands[i].Split(';');
            int playerID = ToInt32(args[0]);
            byte[] loc = {(byte)ToInt32(args[1][1]),(byte)ToInt32(args[1][4])};
            //Call function(playerID,loc)
        }
    }
}


