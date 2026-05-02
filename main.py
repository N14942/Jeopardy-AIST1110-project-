from interface import Interface
from gameboard import JeopardyGame

def main():
    game_logic = JeopardyGame()
    ui = Interface(game_logic)

    # Run Main Loop
    ui.run() # Run Function 'run()' in 'interface.py'


if __name__ == "__main__":
    main()
