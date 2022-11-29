# cheap-blue
Thanks for taking the time to check this out! 

The code is for a complete chess game, including a gui with piece sprites and mouse input. A couple screenshots of the gui can be found in the photos folder.\
There are three files of python code: chessboard, window, and main.

Chessboard contains classes for under-the-hood chess logic, defining legal moves and storing the state of the board.\
Window draws the board onscreen, takes input from the user, and refreshes the gui whenever a piece is moved.\
Main is responsible for executing the code defined in window.

Extra features:\
  Square of the selected piece turns red, so you don't accidentally make a move\ 
  If you attempt to make an illegal move it just doesn't work, and the square turns back to normal colors\
  Gui changes dimensions to fit the screen of the user
  
More details can be found in the in-code documentation.
