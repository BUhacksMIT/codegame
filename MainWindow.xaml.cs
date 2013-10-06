using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Threading;
using System.IO;
using System.Timers;
using System.Windows.Threading;
using System.Text.RegularExpressions;

namespace TestBenchTimers
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        int[][] grid;
        DispatcherTimer timer;
        string[] commands;
        int i;
        //long systemTime;
        //Thread t;

        public MainWindow()
        {
            InitializeComponent();
            colorArray(40, 20);
            startGame();
        }//main

        private void dispatcherTimer_Tick(object sender, EventArgs e)
        {
            if (i < commands.Length)
            {
                if (commands[i][0] == '1')
                {
                    //Place a new ship
                    commands[i] = commands[i].Substring(2, commands[i].Length - 3);
                    string[] arguments = commands[i].Split(';');
                    int playerID = Convert.ToInt32(arguments[0]);
                    int[] loc = { (int)Char.GetNumericValue(arguments[1][1]), (int)Char.GetNumericValue(arguments[1][4]) };
                    //Call function(playerID,loc)
                    //Console.Write(playerID); Console.Write(loc[0]); Console.WriteLine(loc[1]);
                    placeShip(playerID, loc);
                }
                else if (commands[i][0] == '2')
                {
                    //Move a ship
                    commands[i] = commands[i].Substring(2, commands[i].Length - 3);
                    string[] arguments = commands[i].Split(';');
                    int playerID = Convert.ToInt32(arguments[0]);
                    int[] loc = { (int)Char.GetNumericValue(arguments[1][1]), (int)Char.GetNumericValue(arguments[1][4]) };
                    int[] newLoc = { (int)Char.GetNumericValue(arguments[2][1]), (int)Char.GetNumericValue(arguments[2][4]) };
                    //Call function(playerID,loc,newLoc)
                    //Console.Write(playerID); Console.Write(loc[0]); Console.WriteLine(newLoc[1]);
                    moveShip(playerID, loc, newLoc);
                }
                else if (commands[i][0] == '3')
                {
                    //Fire at another ship
                    commands[i] = commands[i].Substring(2, commands[i].Length - 3);
                    string[] arguments = commands[i].Split(';');
                    int playerID = Convert.ToInt32(arguments[0]);
                    int[] loc = { (int)Char.GetNumericValue(arguments[1][1]), (int)Char.GetNumericValue(arguments[1][4]) };
                    int[] newLoc = { (int)Char.GetNumericValue(arguments[2][1]), (int)Char.GetNumericValue(arguments[2][4]) };
                    //Call function(playerID,loc,newLoc)
                    //Console.Write(playerID); Console.Write(loc[0]); Console.WriteLine(newLoc[1]);
                    fire(playerID, loc, newLoc);

                }
                else if (commands[i][0] == '4')
                {
                    //Remove a ship from grid
                    commands[i] = commands[i].Substring(2, commands[i].Length - 3);
                    string[] arguments = commands[i].Split(';');
                    int playerID = Convert.ToInt32(arguments[0]);
                    int[] loc = { (int)Char.GetNumericValue(arguments[1][1]), (int)Char.GetNumericValue(arguments[1][4]) };
                    //Call function(playerID,loc)
                    //Console.Write(playerID); Console.Write(loc[0]); Console.WriteLine(loc[1]);
                    removeShip(playerID, loc);
                }
                else if (commands[i][0] == '5')
                {
                    int playerID = Convert.ToInt32(commands[i][2]);
                    endGame(playerID);
                    timer.Stop();
                    return;
                }
                i++;
            }
        }

        void colorArray(int rows, int cols)
        {
            grid = new int[rows][];
            for (int r = 0; r < grid.Length; r++)
            {
                grid[r] = new int[cols];
            }
            for (int i = 0; i < grid.Length; i++)
            {
                for (int j = 0; j < grid[i].Length; j++)
                {
                    grid[i][j] = 0;
                }
            }
        }

        void placeShip(int playerID, int[] loc)
        {
            grid[loc[0]][loc[1]] = playerID;
            this.debugBox.Text += "Ship placed\r\n";
        }

        void moveShip(int playerID, int[] loc, int[] newLoc)
        {
            grid[loc[0]][loc[1]] = 0;
            grid[newLoc[0]][newLoc[1]] = playerID;
            this.debugBox.Text += "Ship moved\r\n";
            //Implement moving graphic
        }

        void fire(int playerID, int[] loc, int[] newLoc)
        {
            //Implement missile graphic
            this.debugBox.Text += "Missile fired\r\n";
        }

        void removeShip(int playerID, int[] loc)
        {
            grid[loc[0]][loc[1]] = 0;
            //Implement blow up graphic
            this.debugBox.Text += "Ship removed\r\n";

        }

        void endGame(int playerID)
        {
            //Display the winner
            this.debugBox.Text += "Game over\r\n";
        }

        protected void startGame()
        {
            string log;
            string myPath = System.Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            if (System.IO.Directory.Exists(myPath + @"\log"))
            {
                log = File.ReadAllText(myPath + @"\log" + @"\log.txt");
                string newLine = "\r\n";
                commands = Regex.Split(log, newLine);
                timer = new System.Windows.Threading.DispatcherTimer();
                timer.Tick += new EventHandler(dispatcherTimer_Tick);
                timer.Interval = new TimeSpan(0, 0, 0, 1);
                timer.Start();
            }
        }
    }//partial class
}//namespace
