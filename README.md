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


[Completeness] Issue with Require Corners Rule
Test 26 (test_require_own_corners_1()) was not comprehensive yet. We added lines 794-798 in tests/test_blokus.py to ensure that the player could not place another piece without sharing corners where that piece could take the shape of any of the remaining shapes. 


[Completeness] Issue with Available Moves
There was a minor issue with the method legal_to_place() with the exact values 
it was iterating through, thus returned the wrong values to available_moves(). 
We changed line 287 from "range(c - 1, r + 2)" to "range(c - 1, c + 2)", which 
fixed the issue.

### GUI

### TUI

### Bot
This component received two S scores in Milestone 2.

### QA