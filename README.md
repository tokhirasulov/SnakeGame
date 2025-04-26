
# Snake Game with Hand Tracking

This project implements a **Snake Game** where the player controls the snake's movement using hand gestures, specifically by moving their hand in front of the camera. The game is built using **OpenCV**, **cvzone**, **pygame**, and **HandTracking**.

### Purpose
The purpose of this project is to combine computer vision, hand tracking, and game development to create an interactive experience where the player can control the classic **Snake Game** using hand gestures. The game uses the **HandDetector** module to detect hand movements and translate them into snake movements.

### Features:
- Hand gesture-based snake control.
- Snake grows longer as it eats food.
- The game ends if the snake collides with itself.
- Option to restart the game by raising the index finger.

### Requirements

To run this project, you need to have the following dependencies installed:

- **Python 3.x**
- **OpenCV** (for computer vision)
- **cvzone** (for hand tracking and drawing)
- **pygame** (for playing sounds)
- **numpy** (for handling arrays)

You can install the required libraries using the following command:

```bash
pip install opencv-python cvzone pygame numpy
```

Additionally, make sure to have the following files in your project directory:
- **"eat.wav"**: The sound that plays when the snake eats food.
- **"game_over.wav"**: The sound that plays when the game ends.
- **"linkedin.png"**: The image used as the food in the game (you can replace this with any image you like).

### How to Run the Game

1. Clone the repository or download the project files to your local machine.

2. Make sure you have a webcam connected to your system.

3. Place the sound files (`eat.wav` and `game_over.wav`) and the food image (`linkedin.png`) in the same directory as your script.

4. Open a terminal and navigate to the directory where the project files are located.

5. Run the following command to start the game:

```bash
python snake_game.py
```

6. **Gameplay**:
   - Move your hand in front of the camera to control the snake.
   - The game will end if the snake collides with itself.
   - Raise your index finger to restart the game after a game over.

7. **Exit the Game**:
   - Press the `q` key to quit the game.

### Game Controls

- **Snake Movement**: Move your hand in front of the camera. The snake follows the movement of your index finger.
- **Restart Game**: Raise your index finger after the game ends to restart the game.
- **Quit Game**: Press the `q` key.

### Troubleshooting

- Ensure that your webcam is functioning correctly and that it is not being used by any other application.
- If the game is too slow or unresponsive, check your system's resources to ensure that the computer vision processing can run smoothly.
