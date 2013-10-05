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
 
fileInfo= new FileInfo(fileName);

string log;
string myPath = fileInfo.DirectoryName;;
if (System.IO.Directory.Exists(myPath+@"\log")) {
    string log = File.ReadAllText(myPath+@"\log"+@"\log.txt");
    char newLine = "\r\n";
    string[] commands = log.Split(newLine);
    for (int i = 0; i < commands.Length; i++) {
    }
}


