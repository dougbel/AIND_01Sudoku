# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Without taking the advantage of constraint propagation a search procedure consist in a bigger set of posibilities.
As two boxes in a unit have as possible values the same two values (and only this two values), it's logical that any other boxes are not able of having them as possibles values.
The same happen for three boxes with three possible values in the same unit. The problem here is that this triplets is a situations that doesn't happen commonly.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: As in the last question.Without taking the advantage of constraint propagation a search procedure consist in a bigger set of posibilities.
What we are doing in this kind of Sudoku is adding constrains. In every diagonal sudoku there are two units more to add, one by every principal diagonal in board.
As in other units the solution of Sudoku haven't repeated digits in those principal diagonals.
In these kind of sudokus the search procedure is reduced in the number of posibilities because  of this restriction.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.