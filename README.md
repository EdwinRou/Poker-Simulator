# Poker Game Simulator 🃏

Welcome to the **Poker Game Simulator**, a Python-based program designed to simulate a poker game with support for betting, player actions, and hand evaluation. This project provides a modular structure to handle the complexities of poker gameplay, including card dealing, betting rounds, and determining winners.

---

### Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [How to Play](#how-to-play)
- [Game Rules](#game-rules)
- [Game Structure](#game-structure)
- [Core Classes](#core-classes)
- [Customization](#customization)
- [Testing and Validation](#testing-and-validation)
- [Future Improvements](#future-improvements)

## Features
- **Deck and Card Management**: Automatically shuffles a deck of 52 cards and handles dealing cards to players.
- **Player States**: Tracks player states such as waiting, in-hand, or folded.
- **Betting Rounds**: Supports betting phases like pre-flop, flop, turn, and river.
- **Hand Evaluation**: Determines the best 5-card poker hand for each player using poker hand rankings.
- **Showdown**: Determines the winner(s) or handles ties in a poker round.
- **Bot Players**: players with random decision-making.
- **Blind System**: Implements small and big blinds with rules for blind progression over rounds.
- **Docker Support**: Easily run the simulator in a Dockerized environment.

---

## Requirements
- Python 3.8+
- Standard Python libraries (`random`, `itertools`, `dataclasses`, `enum`)
- Optional: [Docker](https://www.docker.com/) for containerized execution.

---

## How to Play

### Starting the Game
1. Clone the repository and navigate to the project folder.
2. **Run Locally**:
   ```bash
   python sources/main.py
    ```
3. **Run Using Docker**:
   - Build the Docker image:
     ```bash
     docker build -t poker-simulator .
     ```
   - Run the container:
     ```bash
     docker run -it poker-simulator
     ```

By default, the game is set up with three players, all controlled by AI bots.

---

## Game Rules
- Each player starts with a fixed number of blinds (`initial_stack`).
- The game progresses through rounds, with blinds increasing after a set number of rounds.
- Players take turns betting, calling, raising, or folding based on their cards and the current pot.
- The last remaining player or the player with the best hand at showdown wins the pot.

---

## Game Structure
1. **Table Initialization**:
   - Players are created with unique IDs and stacks.
   - A random player is assigned as the dealer.

2. **Betting Rounds**:
   - **Pre-Flop**: Players are dealt two cards each.
   - **Flop**: Three community cards are dealt.
   - **Turn**: One additional community card is dealt.
   - **River**: One final community card is dealt.

3. **Showdown**:
   - The best 5-card hand is evaluated for each player still in the game.
   - The winner(s) receive the pot.

4. **Blind System**:
   - Blinds are updated based on a specified rule (e.g., every 10 rounds, blinds increase by 1.5x).

5. **End of Game**:
   - The game ends when only one player has chips remaining.

---

## Core Classes

### `Card` and `Deck`
- Manages the standard 52-card deck.
- Shuffles and deals cards to players.

### `Player`
- Represents each player, tracking their stack, state, and actions.
- Supports betting, folding, and resetting between rounds.

### `Table`
- Manages the game setup, player order, and blind progression.

### `Round`
- Orchestrates a complete poker round, from dealing cards to the showdown.

### `BettingRound`
- Handles individual betting phases within a round.

---

## Customization

### Adding Players
You can add more players or customize player settings by modifying the `player_names` and other parameters in the `main` function:
```python
player_names = [
    ("Player1", True),  # Human Player
    ("Bot1", False),    # AI Bot
    ("Bot2", False)     # Additional AI Bot
]
```
- **Stacks**: Adjust the `initial_stack` parameter in the `Table` initialization to set each player's starting chips.
- **Player Types**: Change the second value in the tuple to `True` for human players or `False` for AI-controlled players.

---

### Adjusting Game Settings
Modify the following parameters in the `Table` initialization:
- `initial_blind`: Starting value of the blinds.
- `blind_rule`: Tuple `(rounds_to_increase, multiplier)` for blind progression.
- `initial_stack`: Starting stack size for each player.

---

## Testing and Validation
The code includes several unit tests to ensure core functionality, such as:
- Validating the deck initialization.
- Ensuring proper card dealing.
- Verifying betting logic and player state transitions.

---

## Future Improvements
- add a good UI
- Enhanced AI decision-making based on hand evaluation and pot odds.
- Online multiplayer functionality.

---

Enjoy your game! 🃏
