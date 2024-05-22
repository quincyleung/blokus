# CMSC 14200 Course Project

Team members:
- GUI: Sean Choi (schoi12)
- TUI: Minseo Kim (mkim27)
- Bot: Quincy Leung (quincyleung)
- QA: Grace Lu (ggracelu)

## Improvements
### Game Logic
[Completeness] Issue with Shape Loading
There was an issue with the method from_string() from the class Shape
with how it was determining the shape squares. We updated lines 114-157 
accordingly.

[Completeness] Issue with Start Positions
There was an issue with the start positions for Blokus Mini configurations. The expected start positions in test_init_blokus_mini_1() and test_init_blokus_mini_2() were changed from 5 start positions to 2 start positions, as clarified by the updated description of the Blokus Mini game configuration in the Blokus Specification. We updated line 25 and 42 in tests/test_blokus.py accordingly.

[Completeness] Issue with Require Corners Rule
Test 26 (test_require_own_corners_1()) was not comprehensive yet. We added lines 794-798 in tests/test_blokus.py to ensure that the player could not place another piece without sharing corners where that piece could take the shape of any of the remaining shapes. 

[Completeness] Issue with Available Moves
There was a minor issue with the method legal_to_place() with the exact values 
it was iterating through, thus returned the wrong values to available_moves(). 
We changed line 287 from "range(c - 1, r + 2)" to "range(c - 1, c + 2)", which 
fixed the issue.

### GUI

[Code_Quality] Added doc strings 

[Completeness] Running python3 src/{g,t}ui.py 20 doesn’t correctly display the board, start positions, and initial randomly selected piece, Same as previous but for python3 src/{g,t}ui.py duo, Same as previous but for python3 src/{g,t}ui.py mono:

Fixed all and went through all listed parameters using click methods. Added a main function and set default variables to make sure every input listed on canvas was functional 

[Completeness] Pending Piece Display not completed as required

Instead of taking the squares of pending piece from shape.squares and trying to shift each square, I now use the squares() method which returns the accurate squares and just change the anchors instead. Now the pending piece (hovering in my case) will place exactly where it was hovering and no longer starts outside of the frame.

[Completeness] Current Player Display not completed as required

I added within the board the necessary display for every single player. Remainig pieces now highlights if in remaining shapes or grey if it's not in remaining shapes. Displays winner at the end but current player turn before then. Displays scores and retired players. 

[Completeness] Random Piece Selection not completed as required
No longer random because now you can choose either by pressing keys or clicking on remaining shapes.

[Completeness] Escape Key not completed as required

Implemented escape key so now it quits when escape key is pressed


### TUI
[Completeness] Game modes not displaying boards properly
Mono, Duo, and specified board sizes can create Blokus instances with the given board specifications. 
Overall code is also re-organized to have an overarching TUI class with the blokus attribute and to create Blokus
objects of these game modes inside the constructor.

[Completeness] Display Issues
(Before changing parts of the main function's screen and wrappers, which are currently causing last-minute errors) 
display shows the board and piece being played. Piece is also randomly chosen for each player.

[Completeness] Arrow, Enter, and Escape Keys
Keys and their effect on the shape has been implemented.


### Bot
This component received two S scores in Milestone 2.

### QA
This component received two S scores in Milestone 2.

