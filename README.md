# cheap-blue
Thanks for actually checking this out! I didn't think anyone would, so apologies if the readme is a bit short. 

The code is for a complete chess game and gui with piece sprites and mouse input
There are three files of python code, chessboard, window, and main
Chessboard contains classes for under-the-hood chess logic, defining legal moves and storing the state of the board
Window draws the board onscreen, and takes input. 
Main basically just calls the window.

Extra features: 
  Square of the selected piece turns red, so you don't accidentally make a move 
  If you attempt to make an illegal move it just doesn't work, and the square turns back to normal colors
  Gui resizes based on screen of the user

This is a huge oversimplication-the in-code documentation is much more complete
