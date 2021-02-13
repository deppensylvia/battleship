#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 13:09:34 2021
Battleship
Program for two players to play the game of battleship with each other
@author: sylviadeppen
"""

"""
GAME INSTRUCTIONS:
    Two player will place their ships (see fleet below) on a 10 x 10 grid
    without the other player knowing the location of the ships.
    They will take turns guessing locations if the ships on each other's boards
    The first player to guess all the locations of their opponent's ships will win.
    
FLEET
5 spots = (a) Aircraft Carrier
4 spots = (b) Battleship
3 spots = (s) Submarine
3 spots = (d) Destroyer
2 spots = (c) Cruiser
"""
from os import system, name 
import copy

"""
GAME INITIATION
Create empty player board
"""
def reset_board():
    empty_board = [["-" for spot in range(10)] for col in range(10)]
    return empty_board


"""
VIEW BOARD
prints out a player's board to the console
"""
def view_board(player):
    letters = [chr(65 + a) for a in range(10)]
    numbers = [str(a) for a in range(1,11)]
    print("  ", "  ".join(numbers))
    count = 0
    for x in player:
        print(letters[count], "", "  ".join(x))
        count += 1
    print("\nKey: '-' = empty spot, 'X' = a hit ship, '.' = a missed guess")
        

        
"""
CHECK VALIDITY OF SETTING SPOT
"""    
def check_coordinates(player, coordinates, setting_board): 
    #check for valid coordinates  
    try:
        row = ord(coordinates[0].upper()) - 65
        col = int(coordinates[1:]) - 1
    except:
        print("Incorrect input format of location")
        return False, None, None
    
    #check if location is valid
    if row >= 10 or row < 0 or col >= 10 or col < 0:
        print("Invalid row or column")
        return False, None, None
    if setting_board:
        if player[row][col] != '-':
            print("Location taken")
            return False, None, None   
    return True, row, col
    
def check_valid_spot(player, coordinates, direction, ship):
    #Convert spot to position on board and check if valid
    
    valid_coordinates, row, col = check_coordinates(player, coordinates, True)
    
    if not valid_coordinates:
        return False

    #check if direction is valid
    direction_list = ['LEFT', 'RIGHT', 'UP', 'DOWN', 'U', 'D', 'L', 'R']
    direction = direction.upper()
    if direction.upper() not in direction_list:
        print("Incorrect format of direction")
        return False
    
    for length in range(fleet[ship][0]):
        try:
            #check up
            if direction == 'RIGHT' or direction == 'R':
                if player[row][col + length] != '-':
                    print("coordinates out of bounds")
                    return False
        
            #check down
            if direction == 'LEFT' or direction == 'L':
                if player[row][col - length] != '-' or col - length < 0:
                    print("coordinates out of bounds")
                    return False
            
            #check left
            if direction == 'UP' or direction == 'U':
                if player[row  - length][col] != '-' or row - length < 0:
                    print("coordinates out of bounds")
                    return False
            
            #check right
            if direction == 'DOWN' or direction == 'D':
                if player[row + length][col] != '-':
                    print("coordinates out of bounds")
                    return False
        except:
            print("coordinates out of bounds")
            return False
        
    for length in range(fleet[ship][0]):
        #add ship to board in up direction
        if direction == 'RIGHT' or direction == 'R':
            player[row][col + length] = ship
    
        #add ship to board in down direction
        if direction == 'LEFT' or direction == 'L':
            player[row][col - length] = ship
        
        #add ship to board in left direction
        if direction == 'UP' or direction == 'U':
            player[row  - length][col] = ship
        
        #add ship to board in right direction
        if direction == 'DOWN' or direction == 'D':
            player[row + length][col] = ship

    return True
        
"""       
SET FLEET
"""
def set_fleet(player):
    for x in fleet:
        spot = input("Pick coordinates for your " + fleet[x][1] + \
                         " {" + str(fleet[x][0])+ "} units long (i.e. 'A5' or 'D8'): ")
        direction = input("Select a direction for your " + fleet[x][1] + "('up', 'down', 'left', 'right'): ")
        while not check_valid_spot(player, spot, direction, x):
            print("Please try again.")
            spot = input("Pick coordinates for your " + fleet[x][1] + \
                         " {" + str(fleet[x][0])+"} units long (i.e. 'A5' or 'D8'): ")
            direction = input("Select a direction for your " + fleet[x][1] + " ('up', 'down', 'left', 'right'): ")
        view_board(player)
    return 


"""
CLEAR SCREEN
"""
# define our clear function 
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')
        
"""
CHECK PLAYER'S GUESS
"""
def guess_location(opponent, player_guesses, coordinates, opponent_fleet):
    valid_coordinates, row, col = check_coordinates(opponent, coordinates, False)
    #check for valid guess
    while not valid_coordinates:
        coordinates = input("Please enter valid coordinates: ")
        valid_coordinates, row, col = check_coordinates(opponent, coordinates, False)
     
    #picked an already guessed spot    
    while player_guesses[row][col] == 'X' or player_guesses[row][col] == '.':
        coordinates = input("You've already guess that spot. Try again: ")
        valid_coordinates, row, col = check_coordinates(opponent, coordinates, False)
        while not valid_coordinates:
            coordinates = input("Please enter valid coordinates: ")
            valid_coordinates, row, col = check_coordinates(opponent, coordinates, False)
            
    #picked a ship's location        
    if opponent[row][col] in opponent_fleet:
        player_guesses[row][col] = 'X'
        ship = opponent[row][col]
        opponent_fleet[ship][0] = opponent_fleet[ship][0] - 1
        print("Hit!")
        if opponent_fleet[ship][0] == 0:
            print("You sunk your opponent's", opponent_fleet[ship][1])
        return 1
    
    #picked an empty spot
    else:
        player_guesses[row][col] = '.'
        print("You missed...")
        return 0

"""
START GAME
"""
#defined here in case we want to add/substract ships to game
FLEET = ({'a' : [5, "Aircraft Carrier"],
          'b' : [4, "Battleship"],
          's' : [3, "Submarine"],
          'd' : [3, "Destroyer"],
          'c' : [2, "Cruiser"]
         },)
while True:
### Initiate new game
    winning_hit_count = 0 #number of hits it takes to win
    fleet = FLEET[0]
    for i in fleet: 
        winning_hit_count += fleet[i][0]
    player1_score = 0
    player2_score = 0      
    player1, player2, = reset_board(), reset_board()
    player1_guesses, player2_guesses = reset_board(), reset_board() 
    player1_fleet = copy.deepcopy(fleet)
    player2_fleet = copy.deepcopy(fleet)
### -----------------
    print("Player 1, set your board.")
    view_board(player1)
    set_fleet(player1)
    clear()
    
    print()
    view_board(player2)
    print("Player 2, set your board.")
    set_fleet(player2)
    clear()
    
    while True:
        print()
        print("***PLAYER 1's TURN***")
        view_board(player1_guesses)
        coordinates = input("Player 1's turn. Guess your opponent's coordinates (i.e. 'A5' or 'D8'): ")
        player1_score += guess_location(player2, player1_guesses, coordinates, player2_fleet)
        if player1_score == winning_hit_count:
            print("Player 1 wins!")
            break
        
        print()
        print("***PLAYER 2's TURN***")
        view_board(player2_guesses)
        coordinates = input("Player 2's turn. Guess your opponent's coordinates (i.e. 'A5' or 'D8'): ")
        player2_score += guess_location(player1, player2_guesses, coordinates, player1_fleet)
        if player2_score == winning_hit_count:
            view_board(player1)
            print("Player 2 wins!")
            break
        
    print("Player 1's board: ")
    view_board(player1)
    print()
    print("Player 2's board: ")
    view_board(player2)
    print()
    
    restart = input("Play again? (Y/N)")
    if restart not in ['Y', 'y', 'Yes', 'yes', 'YES']:
        break
    
print("Thanks for playing!")
    
