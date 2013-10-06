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

namespace game_interface
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            //define the size of the grid
            const int rows = 40, cols = 20;

            //create the grid:    
            createGrid(rows,cols);
           
            //place an object in it...currently a rectangle(future version will let you pass the actual object)
            placeObj(1, 3, rows, cols);

            //place image
            placeIM();
            




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

        void placeObj( double x, double y, double rows, double cols)
        {


            //define the dimensions of the rectangle based on the # of rows and cols
            double h = GameGrid.Height;
            double w = GameGrid.Width;

            double height_s, width_s;

            height_s = h / rows;
            width_s = w / cols;

            //create the rectangle
            Rectangle shipIM = new Rectangle();

            //set rectangle dimensions
            shipIM.Height = height_s;
            shipIM.Width = width_s;

            //define the looks
            shipIM.Fill = new SolidColorBrush(Colors.Gold);     //face color
            shipIM.StrokeThickness = 2;                         //edge thickness
            shipIM.Stroke = new SolidColorBrush(Colors.Green);  //edge color

            //set the position based on coordinates relative to number of pixels
            double Y_pos = height_s * y;                    
            double X_pos = width_s * x;
            GameGrid.Children.Add(shipIM);
            Canvas.SetBottom(shipIM, Y_pos);
            Canvas.SetLeft(shipIM, X_pos);
           
        }//placeObj


        void placeIM() 
        {   
            Image myship = new Image();
            
            myd;
            
            Uri pathToImage = 

            ImageSource imageSource = new BitmapImage(pathToImage);

            Ship.Source = imageSource;
        
        
        
        
        
        }


        





    }//partial class
}//namespace


    