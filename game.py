"""
415 final project
Haiyu Zhang
last date:12/03/2019
"""
"""
game logic and score log
"""

from random import randint

win = 0
loss = 0


def play(playerChoice):
    global win
    global loss
    choices = ["Rock", "Paper", "Scissors"]
    computer = choices[randint(0, 2)]
    if playerChoice == computer:
        print("Tie!")
    elif playerChoice == "Rock":
        if computer == "Paper":
            print("You lose...", computer, "beats", playerChoice)
            win = win + 1
            loss = loss + 1
        else:
            print("You win!", playerChoice, "beats", computer)
    elif playerChoice == "Paper":
        if computer == "Scissors":
            print("You lose...", computer, "beats", playerChoice)
            loss = loss + 1
        else:
            print("You win!", playerChoice, "beats", computer)
            win = win + 1
    elif playerChoice == "Scissors":
        if computer == "Rock":
            print("You lose...", computer, "beat", playerChoice)
            loss = loss + 1
        else:
            print("You win!", playerChoice, "beat", computer)
            win = win + 1
    else:
        print("That's not a valid move.")


def score():
    if win > loss:
        print("You are winning. You lead " + str(win) + "-" + str(loss))
    elif win < loss:
        print("You are losing. Computer leads " + str(win) + "-" + str(loss))
    else:
        print("Tie!" + str(win) + "-" + str(loss))
