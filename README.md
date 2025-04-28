# Connect 4 Game Playing AI Agents

**Module:** Artificial Intelligence & Machine Learning 1  
**Module Code:** 55-508228  
**Assignment Title:** Connect 4 Game Playing AI Agent  
**Student ID:** 19014005  
**Student Name:** Oladotun A Ogundari  
**Submission Date:** 28th April 2025


# Connect4Game – GUI Version

A Python-based Connect Four game featuring a graphical user interface (GUI) and multiple intelligent AI agents. Built with Pygame, this project allows players to enjoy classic Connect 4 gameplay in several interactive modes, including a pure Human vs Human experience, as well as battles against various AI agents.

## Features

- **GUI-Based Gameplay** using Pygame.
- **Object-Oriented Programming (OOP)** architecture used throughout the project for     clean, maintainable, and scalable code.
- **Game Modes**:
  - Human vs Human: Play against a friend locally.
  - Human vs Random Agent
  - Human vs Smart Agent
  - Human vs MiniMax Agent
  - Human vs ML Agent (ML-based predictions with fallback to Minimax if model is unavailable)
  - AI vs AI: Any combination of AI agents (Random, Smart, Minimax, ML)
- **Turn Timer**: Enforced move delay to prevent multi-click issues.
- **AI Agents Included**:
  - 🔹 RandomAgent: Makes random legal moves.
  - 🔹 SmartAgent: Tries to block or win strategically.
  - 🔹 MiniMaxAgent: Uses Minimax with alpha-beta pruning.
  - 🔹 MLAgent: Uses machine learning on the Connect-4 dataset.
- **Background Music** via `music_player.py`.
- **Register Player Prompt**: Optionally enter your name at the start.
- **Modular Codebase** for easy extensions and improvements.
- **Evalution and ML Retraining** evalution.py.

## Installation & Setup

### Prerequisites

- Python 3.x  
- Pip package manager

### Install Dependencies

```
pip install -r requirements.txt

Running the Game

cd Connect4Assessment
python -B src/connect4/main.py

### Project Structure

Connect4Assessment/
├── assets/                  # Audio files, background music, etc.
├── connect4_dataset/         # ML dataset (.csv) and attribute files (.txt)
├── models/                   # Trained ML model (ml_agent_model.pkl)
├── reports/                  # Reports and documentation
├── src/
│   └── connect4Game/
│       ├── agents/
│       │   ├── random_agent.py
│       │   ├── smart_agent.py
│       │   ├── minimax_agent.py
│       │   ├── ml_agent.py
│       ├── utils/
│       │   ├── board_utils.py
│       │   ├── dataset_loader.py
│       │   ├── evaluation.py
│       │   ├── game_state.py
│       │   ├── game_help.py
│       │   ├── music_player.py
│       │   ├── player_data.py
│       ├── graphics.py
│       ├── constants.py
│       ├── game.py
│       ├── play_game.py
│       ├── main.py
├── 19014005_Oladotun_Video.mp4   
├── .gitignore
├── requirements.txt
├── scores.csv
├── README.md


### Customization

from agents import RandomAgent, SmartAgent, MinimaxAgent, MLAgent

agent1 = SmartAgent()
agent2 = MLAgent()

### Future Improvements

Upgrade MLAgent with a trained neural network.

Add animations and transitions for piece drops.

Add networking support for remote Human vs Human.

Integrate advanced algorithms like Monte Carlo Tree Search (MCTS).

### Acknowledgements

Minimax logic adapted from GeeksforGeeks – Minimax Algorithm (Alpha-Beta Pruning)

Dataset sourced from UCI Machine Learning Repository – Connect-4 Game Data

### GitHub Repository

https://github.com/OlaShu112/Connect4Game

.gitignore

__pycache__/
*.pyc
.venv/
assets/*.wav
models/*.pkl

### requirements.txt

pygame
pandas
numpy
scikit-learn
joblib

### Important Tips
To retrain the ML Agent, delete the old model and start the game:

```
rm models/ml_agent_model.pkl
python -B src/connect4Game/main.py
```

### Testing and Validation

Automated testing and validation of the Connect 4 AI agents was performed using the following script:

```
python -B src/connect4/test_validation.py

### Evaluation

evaluation.py was used to evaluate AI agent performance over multiple games (e.g., Smart vs Random Agent, Minimax vs ML Agent) and calculate win/draw rates automatically.

```
python -B src/connect4/utils/evaluation.py


### Testing ML Agent

The ML Agent was tested by first training on the Connect-4 dataset and then evaluating its performance against both human players and other AI agents (including Minimax). If the model file was missing, the system automatically retrains a new model on startup.

### I vs AI Mode

The AI vs AI feature allows any two AI agents (e.g., Random vs Smart, Minimax vs ML) to play against each other automatically. This was particularly useful for evaluating agent performance in bulk simulations (e.g., 100 games or more).