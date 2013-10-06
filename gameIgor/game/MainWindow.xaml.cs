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


namespace game_interface
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        //set the time to fire
        DispatcherTimer timerFire;
        //Missile starting pos
        double startX, startY;
        //Missile ending pos
        double finX, finY;

        Ellipse shot;

        //# of rows and cols on grid
        const int rows = 20, cols = 20;

        bool vert;
        bool horiz;


        public MainWindow()
        {
            InitializeComponent();
            //define the size of the grid
            

            //create the grid:    
            createGrid(rows,cols);
            

            //place image in coordinate x and y
            Image Player1Ship =  placeIM("Player2",9,9);

            //deleteImage(Player1Ship);

            int[] test = {0,0};
            int[] test2 = {10,19};
            animateFire(test,test2);


                

                

                

               

                

            

            
            




        }//main

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

           
            
            Ship.Source = new BitmapImage(new Uri(@"C://Users\\Igor dePaula\\Documents\\GitHub\\codegame\\game\\game\\sprites\\" + player + ".png"));
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
            timerFire.Interval = new TimeSpan(0, 0, 0, 0, 15);
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

            startX = startX * width_s + width_s / 2;
            startY = startY * height_s + width_s / 2;
            finX = finX * width_s + width_s / 2;
            finY = finY * height_s + width_s / 2;

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

            if (startX <= finX && startY <= finY)
            {
                if (vert)
                {
                    startY += (int)20;

                }
                else if (horiz)
                {
                    startX += (int)20;
                }
                else
                {
                    double slope = (finY - startY) / (finX - startX);
                    startX += (int)10*(10 / slope) / Math.Sqrt((10 / slope) * (10 / slope) + (slope * 10) * (slope * 10));
                    startY += (int)10*(slope * 10) / Math.Sqrt((10 / slope) * (10 / slope) + (slope * 10) * (slope * 10));
                }
                Canvas.SetLeft(shot, startX);
                Canvas.SetBottom(shot, startY);
            }
            else
            {
                shot.Height = 30;
                shot.Width = 30;
                shot.Fill = null;
                timerFire.Stop();
            }
        }


        
    

            
        





    }//partial class
}//namespace


    