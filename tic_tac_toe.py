import random

class TTT_cs170_judge:
    def __init__(self):
        self.board = []
        
    def create_board(self, n):
        for i in range(n):
            row = []
            for j in range(n):
                row.append('-')
            self.board.append(row)
            
    def display_board(self):
        for row in self.board:
            print(" ".join(row))
        print()
            
    def is_winner(self, player):
        # Check rows
        for row in self.board:
            if all([cell == player for cell in row]):
                return True
        
        # Check columns
        for col in range(len(self.board)):
            if all([self.board[row][col] == player for row in range(len(self.board))]):
                return True
        
        # Check diagonals
        if all([self.board[i][i] == player for i in range(len(self.board))]):
            return True
        if all([self.board[i][len(self.board) - i - 1] == player for i in range(len(self.board))]):
            return True
        
        return False
    
    def is_board_full(self):
        return all([cell in ['X', 'O'] for row in self.board for cell in row])
    

class Player_1:
    def __init__(self, judge):
        self.board = judge.board
    
    def my_play(self):
        while True:
            row, col = map(int, input("Enter the row and column numbers separated by space: ").split())
            
            if 1 <= row <= len(self.board) and 1 <= col <= len(self.board[0]):
                self.board[row-1][col-1] = 'X'
                break
            else:
                print("Wrong coordination!")


class Player_2:
    def __init__(self, judge):
        self.judge = judge
        self.board = judge.board

    def my_play(self):
        best_score = float("-inf")
        best_move = None

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == '-':
                    self.board[row][col] = 'O'
                    score = self.calculate_score(self.board)
                    self.board[row][col] = '-'
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        if best_move:
            row, col = best_move
            self.board[row][col] = 'O'
#will check for optimal play without calculating every possibility which is much faster than min max
    def calculate_score(self, board):
        # Check if the AI has won
        if self.judge.is_winner('O'):
            return 1
        # Check if the opponent has won
        elif self.judge.is_winner('X'):
            return -1
        else:
            # If the board is full, it's a tie
            if self.judge.is_board_full():
                return 0

            # Calculate score based on positions and potential winning paths
            score = 0

            # Rows and Columns
            for i in range(len(board)):
                if board[i].count('O') == 2 and board[i].count('-') == 1:
                    score += 10
                if [board[j][i] for j in range(len(board))].count('O') == 2 and \
                        [board[j][i] for j in range(len(board))].count('-') == 1:
                    score += 10

            # Diagonals
            if [board[i][i] for i in range(len(board))].count('O') == 2 and \
                    [board[i][i] for i in range(len(board))].count('-') == 1:
                score += 10
            if [board[i][len(board) - i - 1] for i in range(len(board))].count('O') == 2 and \
                    [board[i][len(board) - i - 1] for i in range(len(board))].count('-') == 1:
                score += 10

            # Center and Corners
            if board[1][1] == 'O':
                score += 5
            if board[0][0] == 'O' or board[0][2] == 'O' or board[2][0] == 'O' or board[2][2] == 'O':
                score += 3

            # Penalize for potential winning moves by the opponent
            # Rows and Columns
            for i in range(len(board)):
                if board[i].count('X') == 2 and board[i].count('-') == 1:
                    score -= 20
                if [board[j][i] for j in range(len(board))].count('X') == 2 and \
                        [board[j][i] for j in range(len(board))].count('-') == 1:
                    score -= 20

            # Diagonals
            if [board[i][i] for i in range(len(board))].count('X') == 2 and \
                    [board[i][i] for i in range(len(board))].count('-') == 1:
                score -= 20
            if [board[i][len(board) - i - 1] for i in range(len(board))].count('X') == 2 and \
                    [board[i][len(board) - i - 1] for i in range(len(board))].count('-') == 1:
                score -= 20

            return score
        
# Main Game Loop
def game_loop():
    n = 3  # Board size
    game = TTT_cs170_judge()
    game.create_board(n)
    player1 = Player_1(game)
    player2 = Player_2(game)
    starter = random.randint(0, 1)
    win = False
    if starter == 0:
        print("Player 1 starts.")
        game.display_board()
        while not win:
            player1.my_play()
            win = game.is_winner('X')
            game.display_board()
            if win:
                print("Player 1 wins!")
                break
            if game.is_board_full():
                print("It's a tie!")
                break

            player2.my_play()
            win = game.is_winner('O')
            game.display_board()
            if win:
                print("Player 2 wins!")
                break
            if game.is_board_full():
                print("It's a tie!")
                break
    else:
        print("Player 2 starts.")
        game.display_board()
        while not win:
            player2.my_play()
            win = game.is_winner('O')
            game.display_board()
            if win:
                print("Player 2 wins!")
                break
            if game.is_board_full():
                print("It's a tie!")
                break
            
            player1.my_play()
            win = game.is_winner('X')
            game.display_board()
            if win:
                print("Player 1 wins!")
                break
            if game.is_board_full():
                print("It's a tie!")
                break

game_loop() 
