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
        int[][] grid;
        string[] colors = {"","red","blue","green","yellow","orange" };

        public MainWindow()
        {
            InitializeComponent();
               //CALL this to create the grid:            
                //createGrid(,);
            colorArray(40, 20);
        }//main

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
        }

        void moveShip(int playerID, int[] loc, int[] newLoc)
        {
            grid[loc[0]][loc[1]] = 0;
            grid[newLoc[0]][newLoc[1]] = playerID;
            //Implement moving graphic
        }

        void fire(int playerID, int[] loc, int[] newLoc)
        {
            //Implement missile graphic
        }

        void placeShip(int playerID, int[] loc)
        {
            grid[loc[0]][loc[1]] = 0;
            //Implement blow up graphic

        }
    }//partial class
}//namespace
