import random
from enum import Enum

class Choice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

def play_game(user_choice):
    choices = [Choice.ROCK, Choice.PAPER, Choice.SCISSORS]
    
    user_choice = Choice[user_choice.upper()]  # Convert the string input to a Choice enum
    computer_choice = random.choice(choices)
    
    # Game logic
    if user_choice == computer_choice:
        return "It's a tie!"
    elif ((user_choice == Choice.ROCK and computer_choice == Choice.SCISSORS) or
          (user_choice == Choice.PAPER and computer_choice == Choice.ROCK) or
          (user_choice == Choice.SCISSORS and computer_choice == Choice.PAPER)):
        return f"You win! {user_choice.name} beats {computer_choice.name}"
    else:
        return f"You lose! {computer_choice.name} beats {user_choice.name}"
