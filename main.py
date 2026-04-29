from interface import Interface
from game import JeopardyGame
from api_manager import QuestionManager

def main():
    # Reset
    qm = QuestionManager()
    game_logic = JeopardyGame(qm)
    ui = Interface()

    # Run Main Loop
    ui.run() # Run Function 'run()' in 'interface.py'

if __name__ == "__main__":
    main()
