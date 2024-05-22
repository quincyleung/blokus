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

