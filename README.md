# CS 142 Final Project: Blokus Game

This repository contains our team implementation of a playable **Blokus** game developed for CMSC 14200: Computer Science with Applications II at the University of Chicago. The project supports multiple interfaces (GUI and TUI), rule enforcement, and a basic game-playing bot.

## Team members:
- GUI: Sean Choi (schoi12)
- TUI: Minseo Kim (mkim27)
- Bot: Quincy Leung (quincyleung)
- QA: Grace Lu (ggracelu)

## 🎮 Features

- Complete game logic for **Blokus** and **Blokus Mini**
- **Graphical UI (GUI)** using Pygame
- **Text-based UI (TUI)** with full keyboard interaction
- Bot player implementation with rule-compliant moves
- Turn-based play with legal move enforcement, corner-checking, and piece tracking
- Support for multiple game modes: mono, duo, and custom board sizes

## 🔧 Game Logic Fixes

- **Shape Loading:** Fixed incorrect square parsing in `Shape.from_string()`  
- **Start Positions:** Adjusted Mini mode start positions from 5 to 2 based on updated spec  
- **Corner Rule:** Improved test coverage to enforce corner-sharing requirement for legal moves  
- **Available Moves:** Corrected iteration range in `legal_to_place()` to fix move generation

## 🖥️ GUI Improvements

- Refactored input handling using `click` CLI framework
- Fixed board and piece display issues across all game modes
- Implemented accurate pending piece preview with `Shape.squares()`
- Visualized current player, remaining pieces, scores, and winner announcements
- Escape key now cleanly exits the game

## 🧾 TUI Improvements

- Structured into a unified `TUI` class with dynamic `Blokus` instance creation
- Fixed rendering issues in mono/duo modes
- Added arrow key navigation, Enter to confirm, and Escape to quit

## 🧠 Bot

- Rule-compliant bot player implemented to simulate autonomous turns
- Integrated into full game loop for testing and play

---

## 📦 How to Run

```bash
# Clone repo and set up virtual environment
git clone https://github.com/quincyleung/blokus.git
cd blokus
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run GUI version
python3 src/gui.py mono

# Run TUI version
python3 src/tui.py mono
