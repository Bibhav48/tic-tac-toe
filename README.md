# Tic-Tac-Toe AI Game

This is a Python-based implementation of the classic Tic-Tac-Toe game, featuring both a human player and an AI opponent. The AI is built using the Minimax algorithm with alpha-beta pruning, ensuring it plays optimally. The game also includes an option for reviewing moves, detecting blunders, and recording gameplay as a video.

## Features

- **Play as X or O**: Users can choose to play as either X or O, while the computer controls the other player.
- **AI Opponent**: The computer opponent uses the Minimax algorithm to determine the best possible move.
- **Blunder Detection**: If a player makes a mistake, the game detects the "blunder" and saves a screenshot highlighting the error.
- **Gameplay Recording**: The game records each match and saves it as a `.mp4` video file for future review.
- **Move Review**: The AI has an optional "review" mode where it can suggest the best move at any given time.
- **Responsive UI**: A simple and responsive Pygame interface, allowing users to make moves via mouse clicks.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/YourUsername/TicTacToe-AI.git
    cd TicTacToe-AI
    ```

2. **Install dependencies**:
    Ensure you have Python installed, then install the required packages using:

    ```bash
    pip install -r requirements.txt
    ```

3. **Download OpenSans Font**:
    Download the `OpenSans-Regular.ttf` font and place it in the root directory.

4. **Setup Environment Variables**:
    Create a `.env` file with the following content:

    ```env
    GAMES=0
    ```

## Running the Game

To start the game, run the `runner.py` file:

```bash
python runner.py
```

### Controls

- **Mouse click** to choose your player (X or O) at the start.
- **Mouse click** on any tile to make a move.
- **Blunder Detection**: If a blunder is detected, a screenshot is saved.
- **Play Again**: Once a game finishes, click the "Play Again" button to start a new match.

### Recorded Files

- Videos of your matches are saved in the `media/` folder as `game_{game_number}.mp4`.
- Blunder screenshots (if any) are saved as `Blunder_game{game_number}.jpeg`.

## File Overview

- **runner.py**: Main file for running the game. Handles user interaction, game rendering, and video recording.
- **tictactoe.py**: Logic file for the Tic-Tac-Toe game, including state initialization, move generation, and AI logic.
- **requirements.txt**: List of Python dependencies for running the project.
  
## Dependencies

- **Pygame**: A library for rendering the game interface and handling user interactions.
- **OpenCV (cv2)**: Used for recording game video.
- **dotenv**: For managing environment variables.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
