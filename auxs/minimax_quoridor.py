from random import getrandbits
import sys
sys.setrecursionlimit(10**7)

def print_winner(winner):
    print(f"Winner is {'X' if winner == 1 else 'O'}!\n")

def check_winner(board): ### True continues
    if 'O' in board[1]:
        return False, -1
    elif 'X' in board[-2]:
        return False, 1
    else: return True, 0


directions = [(1,0),(-1,0),(0,1),(0,-1)]
def get_adyacents(board, pos):
    adyacents = []
    for d in directions:
        ny, nx =pos[0]+d[0], pos[1]+d[1]
        if board[ny][nx]:
            adyacents.append([ny,nx])
    return adyacents


def minimax(board, maximizing, playerO, playerX): #### status (bool(continue/stop), int([-1,1]: W,T,L))
    status = check_winner(board)
    if status[0] == False: ## empate, alguno ganó
        return status[1] ## -1, 1, 0 
    if maximizing:
        best_score = float('-inf')
        for next_pos in get_adyacents(board, playerO):
            board[playerO[0]][playerO[1]] = ' '
            board[next_pos[0]][next_pos[1]] = 'O'
            best_score = max(minimax(board,False, playerO, playerX), best_score)
            board[next_pos[0]][next_pos[1]] = ' '   
            board[playerO[0]][playerO[1]] = 'O'
        return best_score
    else:
        best_score = float('inf')           
        for next_pos in get_adyacents(board, playerX):
            board[playerX[0]][playerX[1]] = ' '
            board[next_pos[0]][next_pos[1]] = 'X'
            best_score = min(minimax(board,True, playerO, playerX), best_score)
            board[next_pos[0]][next_pos[1]] = ' '   
            board[playerX[0]][playerX[1]] = 'X'

        return best_score

def get_best_move(board, maximizing, playerX, playerO): ### 
    best_score = 20
    new_move = []
    if maximizing:
        best_score = float('-inf')
        for next_pos in get_adyacents(board, playerX):
                print(get_adyacents(board,playerX)); input()
                board[playerX[0]][playerX[1]] = ' '
                board[next_pos[0]][next_pos[1]] = 'X'
                s = minimax(board, False, playerO, playerX)
                if best_score < s:
                    best_score = s
                    new_move = next_pos

                board[next_pos[0]][next_pos[1]] = ' '   
                board[playerX[0]][playerX[1]] = 'X'
        return new_move
    else:
        best_score = float('inf')
        for next_pos in get_adyacents(board, playerO):
                board[playerO[0]][playerO[1]] = ' '
                board[next_pos[0]][next_pos[1]] = 'O'
                s = minimax(board, False, playerO, playerX)
                if s < best_score:
                    best_score = s
                    new_move = next_pos

                board[next_pos[0]][next_pos[1]] = ' '   
                board[playerO[0]][playerO[1]] = 'O'
        return new_move


board = [['#','#','#','#','#','#','#'],
         ['#',' ',' ',' ',' ',' ','#'],
         ['#',' ',' ',' ',' ',' ','#'],
         ['#',' ',' ',' ',' ',' ','#'],
         ['#',' ','#','#','#',' ','#'],
         ['#',' ',' ',' ',' ',' ','#'],
         ['#',' ',' ',' ',' ',' ','#'],
         ['#',' ',' ',' ',' ',' ','#'],
         ['#','#','#','#','#','#','#']]
def pb(board): 
    for i in board: print(i)

playerX = [1 , (len(board[0])-1)//2]
playerO = [len(board)-2, (len(board[0])-1)//2]
print(playerX, playerO)
input()
turn = bool(getrandbits(1)) ### turn 1 ai turn -1 player
while check_winner(board)[0]:
    print()
    board[playerO[0]][playerO[1]] = 'O'
    board[playerX[0]][playerX[1]] = 'X'
    pb(board)

    if turn: 
        print("X turn: ")
        playerX = get_best_move(board,True, playerX,playerO)
        print("X finished")
    else: 
        print("O turn: ")
        playerO = get_best_move(board,False, playerX,playerO)
        print("O finished")
    
    w = check_winner(board)
    if w[0] == False: 
        if w[1] != 0: print_winner(w[1])
        else: print("It's a tie!")

    turn = not turn