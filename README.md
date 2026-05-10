# Jeopardy-AIST1110-project-
This is a Jeopardy Game(AIST1110-project).

Main function:

1, Use OpenAI API to generate multiple choices.

2, Create AIPlayers with human-like habits and different ability, which can answer questions, select questions and buzz.

3, Include multiple rounds: JEOPARDY, Double JEOPARDY and Final JEOPARDY.

4, Characteristic function: support difficulty change and customize field.

Functions of different files:

Player.py: Store class AIPlayer and HumanPlayer.

Question.py: Store AIManager and Question class (Store question information and generate questions.)

Gameboard.py: Store class Gameboard for managing multiple players and questions.

interface.py: Store class interface and primitive class button, which onitor and get players' input, and make visual and sound effects. 

setting.py: Store class Sessions, which runs the game using above classes.

Game_flow.txt: Store rules and process of game running.

Folder: music: Store music resources.

Folder: assets: Store art resources.