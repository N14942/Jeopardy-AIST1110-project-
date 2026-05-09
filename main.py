from interface import Interface
from gameboard import Gameboard

class Round:
    def __init__(self, gameboard: Gameboard, interface: Interface):
        self.game = gameboard
        self.interface = interface



def main():
    game_logic = Gameboard()
    ui = Interface(game_logic)

    # Run Main Loop
    ui.run() # Run Function 'run()' in 'interface.py'


if __name__ == "__main__":
    main()
