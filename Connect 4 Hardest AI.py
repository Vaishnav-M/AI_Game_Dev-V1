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
    return 0 <= col < len(board[0]) and board[0][col] == ' '


def get_next_open_row(board, col):
    if not is_valid_column(board, col):
        return None
    for r in reversed(range(len(board))):
        if board[r][col] == ' ':
            return r
    return None


def check_win(board, piece):
    # Horizontal
    for r in range(len(board)):
        for c in range(len(board[0]) - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Vertical
    for r in range(len(board) - 3):
        for c in range(len(board[0])):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Diagonal positive
    for r in range(len(board) - 3):
        for c in range(len(board[0]) - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # Diagonal negative
    for r in range(3, len(board)):
        for c in range(len(board[0]) - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    return False


def evaluate_position(board, piece, opponent_piece):
    score = 0
    center = [row[len(board[0]) // 2] for row in board]
    score += center.count(piece) * 3

    # Horizontal
    for r in range(len(board)):
        row_arr = board[r]
        for c in range(len(row_arr) - 3):
            window = row_arr[c:c + 4]
            score += window.count(piece) * 10
            score -= window.count(opponent_piece) * 8

    # Vertical
    for c in range(len(board[0])):
        col = [board[r][c] for r in range(len(board))]
        for r in range(len(col) - 3):
            window = col[r:r + 4]
            score += window.count(piece) * 10
            score -= window.count(opponent_piece) * 8

    # Diagonal positive
    for r in range(len(board) - 3):
        for c in range(len(board[0]) - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += window.count(piece) * 10
            score -= window.count(opponent_piece) * 8

    # Diagonal negative
    for r in range(3, len(board)):
        for c in range(len(board[0]) - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += window.count(piece) * 10
            score -= window.count(opponent_piece) * 8

    return score


def computer_move(board, computer_piece, human_piece, depth=4):
    def minimax(temp_board, depth, alpha, beta, maximizing_player):
        valid_moves = [c for c in range(7) if is_valid_column(temp_board, c)]

        terminal = check_win(temp_board, computer_piece) or check_win(temp_board, human_piece)
        if depth == 0 or terminal or not valid_moves:
            if terminal:
                if check_win(temp_board, computer_piece):
                    return (None, 100000000)
                elif check_win(temp_board, human_piece):
                    return (None, -100000000)
                else:  # Game over
                    return (None, 0)
            else:  # Depth zero
                return (None, evaluate_position(temp_board, computer_piece, human_piece))

        if maximizing_player:
            value = -float('inf')
            column = random.choice(valid_moves)
            for col in valid_moves:
                row = get_next_open_row(temp_board, col)
                if row is None:
                    continue
                b_copy = [r.copy() for r in temp_board]
                drop_piece(b_copy, row, col, computer_piece)
                new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = float('inf')
            column = random.choice(valid_moves)
            for col in valid_moves:
                row = get_next_open_row(temp_board, col)
                if row is None:
                    continue
                b_copy = [r.copy() for r in temp_board]
                drop_piece(b_copy, row, col, human_piece)
                new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    valid_moves = [c for c in range(7) if is_valid_column(board, c)]
    if not valid_moves:
        return None
    best_col, _ = minimax(board, depth, -float('inf'), float('inf'), True)
    return best_col if best_col is not None else random.choice(valid_moves)


def play_game():
    board = create_board()
    game_over = False

    print("Choose game mode:")
    print("1. Human vs Computer")
    print("2. Human vs Human")
    mode = input("Enter choice (1/2): ").strip()

    human = 'X'
    computer = 'O'
    current_player = human

    while not game_over:
        print_board(board)

        if mode == '1' and current_player == computer:
            print("Computer's turn...")
            col = computer_move(board, computer, human)
            if col is None:
                print("No valid moves left!")
                break
            print(f"Computer chose column {col}")
        else:
            try:
                col = int(input(f"Player {current_player} (0-6): "))
            except ValueError:
                print("Invalid input! Enter a number 0-6")
                continue

        if 0 <= col < 7:
            if is_valid_column(board, col):
                row = get_next_open_row(board, col)
                if row is None:
                    print("Column full!")
                    continue
                drop_piece(board, row, col, current_player)

                if check_win(board, current_player):
                    print_board(board)
                    if mode == '1' and current_player == computer:
                        print("Computer wins!")
                    else:
                        print(f"Player {current_player} wins!")
                    game_over = True
                elif all(' ' not in row for row in board):
                    print_board(board)
                    print("It's a tie!")
                    game_over = True
                else:
                    current_player = computer if current_player == human else human
            else:
                print("Column full!")
        else:
            print("Invalid column number!")


if __name__ == "__main__":
    play_game()