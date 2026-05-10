# AI-Powered Jeopardy! ***AIST1110 GROUP PROJECT***
This group project is created as a version of the television game show Jeopardy! using artificial intelligence, and as the final project for the AIST1110 course.

## Key Features
**[ Question Generation via AI ]** 

Use of Azure OpenAI to create real-time multiple-choice questions based on the selected categories and point values.


**[ AI Opponents ]** 

Three levels of difficulty (easy, medium, and hard), along with different levels of accuracy, response time, and strategies for betting, are offered for each type of AI.


**[ 3-Rounds of Play ]**

1. Jeopardy! Round: Standard play with 1 hidden Daily Double

2. Double Jeopardy! Round: Doubled point values with 2 hidden Daily Doubles

3. Final Jeopardy! Round: High-stakes wagering based on a single final category

  
**[ Customizable Options ]** 

Game difficulty levels can be adjusted, and players can enter their own personalized fields to create a customized quiz.



**[ Rich Multimedia User Interface ]** 

This project uses Pygame to create the UI, with a total of 9 different scenes, effective transitions between scenes, background music, and dynamic visual effects.


## Project Structure & Module Overview
The project is built on Object-Oriented Programming (OOP) principles for high maintainability and scalability.


## Core Files

`player.py`: Defines the Player ABC and its subclasses: HumanPlayer and AIPlayer.

`question.py`: Contains AI_Manager (API handling) and Question (data management).

`gameboard.py`: Manages the overall game state, including player rankings and board setup.

`interface.py`: Handles the Pygame GUI, Button classes, and screen rendering logic.

`setting.py`: Contains the Session class, which coordinates all modules to run the game.

`Game_flow.txt`: Detailed documentation of game rules, scoring logic, and round transitions.


## Resource Folders

`/music`: Contains background tracks and sound effects for each round.

`/assets`: Stores visual resources, including buttons and background images.


## How to Run

**[ Install Requirements ]**

  `pip install pygame openai python-dotenv`


**[ Configure API ]**

Place your Azure OpenAI API key in a `.env` file or provide it within the `AI_Manager` initialization.


**[ Start Game ]**

  `python setting.py`

