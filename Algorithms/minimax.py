from random import getrandbits
import numpy as np
### p1 = 'x' = 120 * 3 = 360
### p2 = 'o' = 111 * 3 = 333
 
def check_rows(board): 
    for row in board:
        if not ' ' in row:
            if not 'X' in row: return -1
            if not 'O' in row: return 1
    return 0
def check_cols(board):
    for i in range(3):
        col = [row[i] for row in board]
        if not ' ' in col:
            if not 'X' in col: return -1
            if not 'O' in col: return 1
    return 0
def check_diagonals(board):
    d1 = []
    d2 = []
    for i in range(3):
        d1.append(board[i][i])
        d2.append(board[2-i][i])
    if not ' ' in d1:
            if not 'X' in d1: return -1
            if not 'O' in d1: return 1
    if not ' ' in d2:
            if not 'X' in d2: return -1
            if not 'O' in d2: return 1
    return 0
    
def valid_move(board, pos):
    if len(pos) == 2:
        if not(0 <= pos[0] and pos[0] < 3 and 0 <= pos[1] and pos[1] < 3):
            print(pos, "Out of bounds"); return False
        if not(board[pos[0]][pos[1]] == ' '):
            print(pos, "Is occupied"); return False
        return True

def print_winner(winner):
    print(f"Winner is {'X' if winner == 1 else 'O'}!\n")

def check_winner(board): ### True continues
    ###  1 = 'X'
    ### -1 = 'O'
    winner = check_rows(board)
    if winner != 0: return False, winner
    winner = check_cols(board)
    if winner != 0: return False, winner
    winner = check_diagonals(board)
    if winner != 0: return False, winner
    else: #tie or continue
        ### board is full
        if any(' ' in row for row in board): return True, 0 ## continue
        else: return False, 0 ## stops

def minimax(board, maximizing): #### status (bool(continue/stop), int([-1,1]: W,T,L))
    status = check_winner(board)
    if status[0] == False:
        return status[1] ## W/L/T case
    if maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    best_score = max(minimax(board,False), best_score)
                    board[i][j] = ' '    
        return best_score

    else:
        best_score = float('inf')           
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    best_score = min(minimax(board, True), best_score)
                    board[i][j] = ' ' 
        return best_score

def get_best_move(board): ### for O
    best_score = float('inf')
    new_move = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                s = minimax(board, True)
                if s < best_score:
                    best_score = s
                    print(best_score)
                    new_move = [i,j]                
                board[i][j] = ' '
    return new_move


board = [[' ',' ',' '],
         [' ',' ',' '],
         [' ',' ',' ']]
def pb(board): 
    for i in board: print(i)
ai = [-1,-1]
player = [-1,-1]
turn = bool(getrandbits(1)) ### turn 1 ai turn -1 player

while check_winner(board)[0]:
    print()
    if turn: 
        print("Player's turn:", end = " ")
        player = [int(x) for x in input().split()]
        if valid_move(board,player): board[player[0]][player[1]] = 'X'
        else: turn = not turn
    else: 
        print("Ai's turn:", end = "\n")
        ai = get_best_move(board)
        if valid_move(board,ai): board[ai[0]][ai[1]] = 'O'
        else: turn = not turn

    pb(board)
    w = check_winner(board)
    if w[0] == False: 
        if w[1] != 0: print_winner(w[1])
        else: print("It's a tie!")
    turn = not turn