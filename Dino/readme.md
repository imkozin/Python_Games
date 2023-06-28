# Google Jumping Dino Game
Welcome to the Google Jumping Dino Game! This is a Python game built using the Pygame library and connected to an external server on Elephant SQL. The game allows users to control a dinosaur character and jump over obstacles to reach higher levels. The user's game results, such as reached levels and received points, are saved in the connected database. Additionally, the game is designed to update the in-game record value whenever a user sets a new high score.

### Usage
1. Launch the game by running dino.py with Python.
2. The game window will open, displaying the dinosaur character and the background.
3. Press any key to start the game. The dinosaur will begin running, and obstacles will appear on the screen.
4. Use the key-up to make the dinosaur jump over the obstacles or the key-down to make the dinosaur ducking.
5. The game ends if the dinosaur collides with an obstacle. The final score and level reached will be displayed.
6. To start a new game, press any key again.
7. The game automatically saves the user's high score in the connected Elephant SQL database.


### Game Controls
* Press the key-up: Make the dinosaur jump.
* Press the key-down: Make the dinosaur duck.

### Database Integration
The Google Jumping Dino Game is integrated with Elephant SQL, an external SQL database service. This integration allows the game to save user results, such as the highest level reached and the corresponding points achieved. Additionally, the game retrieves the current high score from the database and updates the in-game record value whenever a new high score is set.

The db.py file contains the configuration details necessary to connect to your Elephant SQL database. Make sure to update this file with your specific connection information as described in the Installation section.

### Game Video Review 
You can check the video review by clicking [here](https://www.loom.com/share/939bc94445ac4d62971678685c22f8e7?sid=f17b1e71-64ba-4ca5-986b-414034ae6654).