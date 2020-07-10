"""
415 final project
Haiyu Zhang
last date:12/03/2019
"""
"""
main program
"""

import imageprocess


def instructions():
    print(
        "\n\nWelcome to ‘Rock Paper Scissors’!"
        "\nClick on camera window and press 'b' key to set background. "
        "\nMake sure there are no moving objects, in the frame."
        "\nGive your hand gesture in the frame, press 'p' key to play a game."
        "\nPress 'esc' key to exit game.")


def play_game():
    imageprocess.opencamera()


if __name__ == "__main__":
    instructions()
    play_game()
