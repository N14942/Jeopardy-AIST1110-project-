# 🎮 AI-Powered Jeopardy! (AIST1110 Project)
This project is an interactive, AI-driven version of the classic TV quiz show Jeopardy!, developed as a group assignment for the AIST1110 (Introduction to Computing Using Python) course.

## 🚀 Key Features
**[ Dynamic AI Question Generation ]** 

Integrates Azure OpenAI (GPT-4o) to generate real-time multiple-choice questions tailored to specific categories and point values.

**[ Sophisticated AI Opponents ]** 

Features AI players with "human-like" behaviors. They possess different Difficulty levels (Easy, Medium, Hard) that affect their accuracy, reaction time, and wagering strategies.

**[ Full 3-Round Experience ]**

1️⃣ Jeopardy! Round: Standard gameplay with one hidden Daily Double.

2️⃣ Double Jeopardy! Round: Doubled point values with two hidden Daily Doubles.

3️⃣ Final Jeopardy! Round: High-stakes wagering based on a single final category.
  
**[ Customization ]** 

Supports adjustable game difficulty and allows players to input custom fields (categories) for a personalized quiz experience.

**[ Rich Multimedia UI ]** 

Built with Pygame, featuring a 9-scene architecture, smooth transitions, background music, and interactive visual effects.

## 🛠 Project Structure & Module Overview
The project is built on Object-Oriented Programming (OOP) principles for high maintainability and scalability.

## 📄 Core Files
`player.py`: Defines the Player ABC and its subclasses: HumanPlayer and AIPlayer.

`question.py`: Contains AI_Manager (API handling) and Question (data management).

`gameboard.py`: Manages the overall game state, including player rankings and board setup.

`interface.py`: Handles the Pygame GUI, Button classes, and screen rendering logic.

`setting.py`: Contains the Session class, which coordinates all modules to run the game.
`Game_flow.txt`: Detailed documentation of game rules, scoring logic, and round transitions.

## 📂 Resource Folders

`/music`: Contains background tracks and sound effects for each round.

`/assets`: Stores visual resources, including buttons and background images.

## ⚙️ How to Run

**[ Install Requirements ]**

  `pip install pygame openai python-dotenv`

**[ Configure API ]**

Place your Azure OpenAI API key in a `.env` file or provide it within the `AI_Manager` initialization.

**[ Start Game ]**

  `python setting.py`

