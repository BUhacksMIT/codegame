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
using System.Timers;
using System.Windows.Threading;
using System.Text.RegularExpressions;
using System.IO;
using System.Media;
using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System;
using System.Collections;



//FINAL
namespace game_interface
{
    // State object for receiving data from remote device.
    public class StateObject
    {
        // Client socket.
        public Socket workSocket = null;
        // Size of receive buffer.
        public const int BufferSize = 256;
        // Receive buffer.
        public byte[] buffer = new byte[BufferSize];
        // Received data string.
        public StringBuilder sb = new StringBuilder();
    }

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        Image[][] grid;
        //set the time to fire
        DispatcherTimer timerFire;
        DispatcherTimer exploTimer;
        //Missile starting pos
        double startX, startY;
        //Missile ending pos
        double finX, finY;

        double dist;

        double distX;
        double distY;

        Ellipse shot;

        //# of rows and cols on grid
        const int rows = 20, cols = 20;

        bool vert;
        bool horiz;
        bool up;
        bool right;
        Queue myQ;
        Queue mySyncdQ;

        DispatcherTimer timer;
        string[] commands;
        int i;
        int k;


        public MainWindow()
        {
            InitializeComponent();
            //define the size of the grid
            //create the grid:    
            createGrid(rows,cols);
            colorArray(rows,cols);
        }//main

        void colorArray(int rows, int cols)
        {
            grid = new Image[rows][];
            for (int r = 0; r < grid.Length; r++)
            {
                grid[r] = new Image[cols];
            }
            for (int i = 0; i < grid.Length; i++)
            {
                for (int j = 0; j < grid[i].Length; j++)
                {
                    grid[i][j] = null;
                }
            }
        }

        void createGrid(double rows, double cols)
        {

            //First, you need to figure out the dimensions of each square
            double h = GameGrid.Height;
            double w = GameGrid.Width;

            //define the dimensions of the rectangles
            double height_s, width_s;
            height_s = h / rows;
            width_s = w / cols;

            //define colors used for the looks
            Color color1 = Colors.Black;
            Color color2 = Colors.Gray;
           
            //loop to add multiple rectangles
            for (double i = 0; i <= rows*height_s; i += height_s)
                for (double j =0; j <= cols*width_s; j += width_s){

                    Rectangle newonGrid = new Rectangle();

                    //set it on Canvas based on position i and j
                    Canvas.SetBottom(newonGrid, i);
                    Canvas.SetLeft(newonGrid, j);

                    //define dimensions of each field of the grid
                    newonGrid.Width = width_s;
                    newonGrid.Height = height_s;                    
                    
                    //define the looks
                    newonGrid.Fill = new SolidColorBrush(color1);   //face color
                    newonGrid.StrokeThickness = .5;                 //size of the edge
                    newonGrid.Stroke = new SolidColorBrush(color2); //edge color
                    GameGrid.Children.Add(newonGrid);

            }//for
        }//CreateGrid
        
public  void StartClient() {
        // Data buffer for incoming data.
        byte[] bytes = new byte[1024];

        // Connect to a remote device.
        try {
            // Establish the remote endpoint for the socket.
            // This example uses port 11000 on the local computer.
            IPHostEntry ipHostInfo = Dns.Resolve("localhost");
            IPAddress ipAddress = ipHostInfo.AddressList[0];
            IPEndPoint remoteEP = new IPEndPoint(ipAddress,1341);

            // Create a TCP/IP  socket.
            Socket sender = new Socket(AddressFamily.InterNetwork, 
                SocketType.Stream, ProtocolType.Tcp );

            // Connect the socket to the remote endpoint. Catch any errors.
            try {
                sender.Connect(remoteEP);

                Console.WriteLine("Socket connected to {0}",
                    sender.RemoteEndPoint.ToString());

                // Encode the data string into a byte array.
                byte[] msg = Encoding.ASCII.GetBytes("begin");

                // Send the data through the socket.
                int bytesSent = sender.Send(msg);

                // Receive the response from the remote device.
                while (1 == 1)
                {
                    int bytesRec = sender.Receive(bytes);
                    //Console.WriteLine("Echoed test = {0}",
                    //);
                    String resp = Encoding.ASCII.GetString(bytes, 0, bytesRec);
                    mySyncdQ.Enqueue(resp);
                    Thread.Sleep(100);

                }
                // Release the socket.
                sender.Shutdown(SocketShutdown.Both);
                sender.Close();
                
            } catch (ArgumentNullException ane) {
                Console.WriteLine("ArgumentNullException : {0}",ane.ToString());
            } catch (SocketException se) {
                Console.WriteLine("SocketException : {0}",se.ToString());
            } catch (Exception e) {
                Console.WriteLine("Unexpected exception : {0}", e.ToString());
            }

        } catch (Exception e) {
            Console.WriteLine( e.ToString());
        }
    }
        void placeObj(Image shipIM, double x, double y, double rows, double cols)
        {


            //define the dimensions of the rectangle based on the # of rows and cols
            double h = GameGrid.Height;
            double w = GameGrid.Width;

            double height_s, width_s;

            height_s = h / rows;
            width_s = w / cols;

            //create the rectangle

            //set rectangle dimensions
            shipIM.Height = height_s;
            shipIM.Width = width_s;

            

            //set the position based on coordinates relative to number of pixels
            double Y_pos = height_s * y;                    
            double X_pos = width_s * x;
            Canvas.SetBottom(shipIM, Y_pos);
            Canvas.SetLeft(shipIM, X_pos);
           
        }//placeObj


        Image placeIM(string player,double x, double y) 
        {   

            Image Ship = new Image();

            Ship.Name = player;

            Ship.Source = new BitmapImage(new Uri(System.Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + @"\log\" + player + ".png"));
            GameGrid.Children.Add(Ship);

            placeObj(Ship, x, y, 20, 20);

            return Ship;
        
        }

        void deleteImage(Image ship)
        {
            ship.Source = null;
        }

        void blowShip(Image ship)
        { 
        
        
        }

        void animateFire(int[] loc, int[] newLoc)
        {
            startX = (double)loc[0];
            startY = (double)loc[1];
            finX = (double)newLoc[0];
            finY = (double)newLoc[1];
            timerFire = new System.Windows.Threading.DispatcherTimer();
            timerFire.Tick += new EventHandler(moveMissile);
            timerFire.Interval = new TimeSpan(0, 0, 0, 0, 30);
            spawnShot();
            timerFire.Start();

        }

        private void spawnShot()
        {
            double h = GameGrid.Height;
            double w = GameGrid.Width;

            //define the dimensions of the rectangles
            double height_s, width_s;
            height_s = h / rows;
            width_s = w / cols;

            vert = false;
            horiz = false;
            if (startX == finX)
            {
                vert = true;
            }
            if (startY == finY)
            {
                horiz = true;
            }

            up = false;
            right = false;
            if (startX < finX)
                right = true;
            if (startY < finY)
                up = true;

            dist = Math.Sqrt((finX - startX) * (finX - startX) + (finY - startY) * (finY - startY));

            startX = startX * width_s + width_s / 2;
            startY = startY * height_s + width_s / 2;
            finX = finX * width_s + width_s / 2;
            finY = finY * height_s + width_s / 2;

            distX = Math.Abs(finX - startX);
            distY = Math.Abs(finY - startY);

            shot = new Ellipse();
            shot.Fill = new SolidColorBrush(Colors.Gold);
            shot.Width = 12;
            shot.Height = 12;
            Canvas.SetLeft(shot, startX);
            Canvas.SetBottom(shot, startY);
            GameGrid.Children.Add(shot);
        }

        private void moveMissile(object sender, EventArgs e)
        {
            //First, you need to figure out the dimensions of each square

            if ((right && up && (startX <= finX && startY <= finY)) || (!right && up && (startX >= finX && startY <= finY)) || (right && !up && (startX <= finX && startY >= finY)) || (!right && !up && (startX >= finX && startY >= finY)))
            {
                if (vert)
                {
                    if (up)
                        startY += (int)3*dist;
                    else
                        startY -= (int)3*dist;

                }
                else if (horiz)
                {
                    if (right)
                        startX += (int)3*dist;
                    else
                        startX -= (int)3*dist;
                }
                else
                {
                    
                    double chgX = finX - startX;
                    double chgY = finY - startY;
                    double magnitude = Math.Sqrt(chgX * chgX + chgY * chgY);
                    double vx = 3*dist*chgX/magnitude;
                    double vy = 3*dist*chgY/magnitude;
                    startX += vx;
                    startY += vy;
                }
                Canvas.SetLeft(shot, startX);
                Canvas.SetBottom(shot, startY);
                if (Math.Abs(finX - startX) > distX / 2 || Math.Abs(finY - startY) > distY / 2)
                {
                    shot.Height += 2;
                    shot.Width += 2;
                }
                else
                {
                    shot.Height -= 2;
                    shot.Width -= 2;
                }
            }
            else
            {
                shot.Fill = null;
                timerFire.Stop();
            }
        }

        private void dispatcherTimer_Tick(object sender, EventArgs e)
        {
            //if (i < commands.Length)
            //{
            if (mySyncdQ.Count > 0) {
                string test = (string) mySyncdQ.Dequeue();//commands[i];
                if (test[0] == '1')
                {
                    //Place a new ship
                    test = test.Substring(2, test.Length - 3);
                    string[] arguments = test.Split(';');
                    int playerID = Convert.ToInt32(arguments[0]);
                    string[] arg2 = arguments[1].Replace("(", "").Replace(")", "").Split(',');
                    int[] loc = { Convert.ToInt32(arg2[0]), Convert.ToInt32(arg2[1]) };
                    //Call function(playerID,loc)
                    //Console.Write(playerID); Console.Write(loc[0]); Console.WriteLine(loc[1]);
                    placeShip(playerID, loc);
                    updateTimerInterval((int)Char.GetNumericValue(commands[i + 1][0]));
                }
                else if (test[0] == '2')
                {
                    //Move a ship
                    test = test.Substring(2, test.Length - 3);
                    string[] arguments = test.Split(';');
                    int playerID = Convert.ToInt32(arguments[0]);
                    string[] arg2 = arguments[1].Replace("(", "").Replace(")", "").Split(',');
                    int[] loc = { Convert.ToInt32(arg2[0]), Convert.ToInt32(arg2[1]) };
                    string[] arg3 = arguments[2].Replace("(", "").Replace(")", "").Split(',');
                    int[] newLoc = { Convert.ToInt32(arg3[0]), Convert.ToInt32(arg3[1]) };
                    //Call function(playerID,loc,newLoc)
                    //Console.Write(playerID); Console.Write(loc[0]); Console.WriteLine(newLoc[1]);
                    moveShip(playerID, loc, newLoc);
                    updateTimerInterval((int)Char.GetNumericValue(commands[i + 1][0]));
                }
                else if (test[0] == '3')
                {
                    //Fire at another ship
                    test = test.Substring(2, test.Length - 3);
                    string[] arguments = test.Split(';');
                    int playerID = Convert.ToInt32(arguments[0]);
                    string[] arg2 = arguments[1].Replace("(", "").Replace(")", "").Split(',');
                    int[] loc = { Convert.ToInt32(arg2[0]), Convert.ToInt32(arg2[1]) };
                    string[] arg3 = arguments[2].Replace("(", "").Replace(")", "").Split(',');
                    int[] newLoc = { Convert.ToInt32(arg3[0]), Convert.ToInt32(arg3[1]) };
                    //Call function(playerID,loc,newLoc)
                    //Console.Write(playerID); Console.Write(loc[0]); Console.WriteLine(newLoc[1]);
                    fire(playerID, loc, newLoc);
                    updateTimerInterval((int)Char.GetNumericValue(commands[i + 1][0]));

                }
                else if (test[0] == '4')
                {
                    //Remove a ship from grid
                    test = test.Substring(2, test.Length - 3);
                    string[] arguments = test.Split(';');
                    int playerID = Convert.ToInt32(arguments[0]);
                    string[] arg2 = arguments[1].Replace("(", "").Replace(")", "").Split(',');
                    int[] loc = { Convert.ToInt32(arg2[0]), Convert.ToInt32(arg2[1]) };
                    //Call function(playerID,loc)
                    //Console.Write(playerID); Console.Write(loc[0]); Console.WriteLine(loc[1]);
                    removeShip(playerID, loc);
                    updateTimerInterval((int)Char.GetNumericValue(commands[i + 1][0]));
                }
                else if (test[0] == '5')
                {
                    int playerID = (int)Char.GetNumericValue(test[2]);
                    endGame(playerID);
                    timer.Stop();
                    return;
                }
                else if (test[0] == '6')
                {
                    int playerID = (int)Char.GetNumericValue(test[2]);
                    eliminate(playerID);
                }
               // i++;
            }
        }

        void placeShip(int playerID, int[] loc)
        {
            //this.debugBox.Text += "Ship placed\r\n";
            if (playerID == 1)
                grid[loc[0]][loc[1]] = placeIM("Player1", (double)loc[0], (double)loc[1]);
            else
                grid[loc[0]][loc[1]] = placeIM("Player2", (double)loc[0], (double)loc[1]);
        }

        void moveShip(int playerID, int[] loc, int[] newLoc)
        {
            //grid[newLoc[0]][newLoc[1]] = playerID;
            //this.debugBox.Text += "Ship moved\r\n";
            //Implement moving graphic
            if (playerID == 1)
            {
                grid[newLoc[0]][newLoc[1]] = placeIM("Player1", (double)newLoc[0], (double)newLoc[1]);
                deleteImage(grid[loc[0]][loc[1]]);
                grid[loc[0]][loc[1]] = null;
            }
            else
            {
                grid[newLoc[0]][newLoc[1]] = placeIM("Player2", (double)newLoc[0], (double)newLoc[1]);
                deleteImage(grid[loc[0]][loc[1]]);
                grid[loc[0]][loc[1]] = null;
            }

        }

        void fire(int playerID, int[] loc, int[] newLoc)
        {
            //Implement missile graphic
            //this.debugBox.Text += "Missile fired\r\n";
            animateFire(loc, newLoc);
            playFire();

        }

        void removeShip(int playerID, int[] loc)
        {
            explosion(grid[loc[0]][loc[1]]);
            grid[loc[0]][loc[1]] = null;
            playExplode();
            //Implement blow up graphic
            //this.debugBox.Text += "Ship removed\r\n";
        }

        void endGame(int playerID)
        {
            //Display the winner
            //this.debugBox.Text += "Game over\r\n";
            this.inputConsole.Text = "Player " + playerID.ToString() + " is the winner.";
        }

        void eliminate(int playerID)
        {
            playExplode();
            //Eliminate a loser, bad coder
            for (int i = 0; i < grid.Length; i++)
            {
                for (int j = 0; j < grid[i].Length; j++)
                {
                    if (playerID == 1)
                    {
                        if (null != grid[i][j] && grid[i][j].Name == "Player1")
                        {
                            explosion(grid[i][j]);
                            grid[i][j] = null;
                        }
                    }
                    else
                    {
                        if (null != grid[i][j] && grid[i][j].Name == "Player2")
                        {
                            explosion(grid[i][j]);
                            grid[i][j] = null;
                        }
                    }
                }
            }
        }

        void startGame()
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
                timer.Interval = new TimeSpan(0, 0, 0, 0, 500);
                timer.Start();
            }
        }

        void updateTimerInterval(int command)
        {
            if (command == 1) //Place
            {
                timer.Interval = new TimeSpan(0, 0, 0, 0, 200);
            }
            else if (command == 2) //Move
            {
                timer.Interval = new TimeSpan(0, 0, 0, 0, 500);
            }
            else if (command == 3) //Fire
            {
                timer.Interval = new TimeSpan(0, 0, 0, 0, 800);
            }
            else if (command == 4) //Remove
            {
                timer.Interval = new TimeSpan(0, 0, 0, 0, 300);
            }
            else if (command == 5) //End
            {
                timer.Interval = new TimeSpan(0, 0, 0, 0, 50);
            }
        }

        void explosion(Image Ship)
        {
            k = 0;
            exploTimer = new System.Windows.Threading.DispatcherTimer();
            exploTimer.Tick += new EventHandler(delegate (Object o, EventArgs a) {
                //snip
                if (k < 12)
                {
                    string animationCounterString = k.ToString();
                    Ship.Source = new BitmapImage(new Uri(System.Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + @"\log\tmp-" + animationCounterString + ".gif"));
                    //Ship.Source = null;
                    k++;
                }
                else
                {
                    Ship.Source = null;
                    exploTimer.Stop();
                }
            });

            exploTimer.Interval = new TimeSpan(0, 0, 0, 0, 50);
            exploTimer.Start();
        }


        private void Execute_Click(object sender, RoutedEventArgs e)
        {
            //get string from text box and write to file
            Thread thread = new Thread(StartClient);
            thread.Start();

            myQ = new Queue();
            mySyncdQ = Queue.Synchronized(myQ);
            startGame();
        }

        private void inputConsole_GotFocus(object sender, RoutedEventArgs e)
        {
            inputConsole.Text = "";
        }

        private void Load_Click(object sender, RoutedEventArgs e)
        {
            string language = this.ChooseCodingLanguage.SelectedIndex.ToString();
        }


        void playExplode()
        {

            SoundPlayer explosion = new SoundPlayer(System.Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + @"\log\bomb.wav");

            explosion.Play();

        }

        void playFire()
        {
            SoundPlayer explosion = new SoundPlayer(System.Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + @"\log\fire.wav");

            explosion.Play();

        }





    }//partial class
}//namespace


    