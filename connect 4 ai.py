import random


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


def computer_move(board, computer_piece, human_piece):
    # First check for winning move
    for col in range(7):
        if is_valid_column(board, col):
            row = get_next_open_row(board, col)
            temp_board = [row.copy() for row in board]
            drop_piece(temp_board, row, col, computer_piece)
            if check_win(temp_board, computer_piece):
                return col

    # Block human's winning move
    for col in range(7):
        if is_valid_column(board, col):
            row = get_next_open_row(board, col)
            temp_board = [row.copy() for row in board]
            drop_piece(temp_board, row, col, human_piece)
            if check_win(temp_board, human_piece):
                return col

    # Choose random valid column
    valid_cols = [c for c in range(7) if is_valid_column(board, c)]
    return random.choice(valid_cols)


def play_game():
    board = create_board()
    game_over = False

    # Game mode selection
    print("Choose game mode:")
    print("1. Human vs Computer")
    print("2. Two Player")
    mode = input("Enter choice (1/2): ")

    human_piece = 'X'
    computer_piece = 'O'

    turn = 0  # X goes first

    while not game_over:
        print_board(board)

        if (mode == '1' and turn % 2 == 0) or mode == '2':
            # Human player's turn
            current_piece = human_piece if turn % 2 == 0 else computer_piece
            try:
                col = int(input(f"Player {current_piece} (0-6): "))
            except ValueError:
                print("Please enter a valid number!")
                continue
        else:
            # Computer's turn
            print("Computer's turn...")
            col = computer_move(board, computer_piece, human_piece)
            print(f"Computer chose column {col}")
            current_piece = computer_piece

        if 0 <= col < 7:
            if is_valid_column(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, current_piece)

                if check_win(board, current_piece):
                    print_board(board)
                    if mode == '1' and current_piece == computer_piece:
                        print("Computer wins!")
                    else:
                        print(f"Player {current_piece} wins!")
                    game_over = True
                elif all(' ' not in row for row in board):
                    print_board(board)
                    print("It's a tie!")
                    game_over = True

                turn += 1
            else:
                print("Column full!")
        else:
            print("Invalid column!")


if __name__ == "__main__":
    play_game()