# Connect Four Game
def create_board(rows=6, cols=7):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    for row in board:
        print('|' + '|'.join(row) + '|')
    print(' ' + ' '.join(str(i) for i in range(len(board[0]))))


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_column(board, col):
    return board[0][col] == ' '


def get_next_open_row(board, col):
    for r in reversed(range(len(board))):
        if board[r][col] == ' ':
            return r
    return None


def check_win(board, piece):
    # Check horizontal
    for r in range(len(board)):
        for c in range(len(board[0]) - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Check vertical
    for r in range(len(board) - 3):
        for c in range(len(board[0])):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Check diagonal (positive slope)
    for r in range(len(board) - 3):
        for c in range(len(board[0]) - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for r in range(3, len(board)):
        for c in range(len(board[0]) - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False


def play_game():
    board = create_board()
    game_over = False
    turn = 0
    players = ['X', 'O']

    while not game_over:
        print_board(board)
        col = int(input(f"Player {players[turn]} (0-6): "))

        if 0 <= col < 7:
            if is_valid_column(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, players[turn])

                if check_win(board, players[turn]):
                    print_board(board)
                    print(f"Player {players[turn]} wins!")
                    game_over = True
                elif all(' ' not in row for row in board):
                    print_board(board)
                    print("It's a tie!")
                    game_over = True

                turn = (turn + 1) % 2
            else:
                print("Column full!")
        else:
            print("Invalid column!")


if __name__ == "__main__":
    play_game()