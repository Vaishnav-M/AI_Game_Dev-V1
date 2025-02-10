import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 900
HEIGHT = 800
SQUARE_SIZE = 100
RADIUS = 45
FPS = 60

# Colors
DARK_BLUE = (25, 42, 86)
BOARD_BLUE = (33, 85, 155)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
HOVER_ALPHA = 120

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 Ultimate")
title_font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 48)
message_font = pygame.font.Font(None, 100)


def create_board():
    return [[None for _ in range(7)] for _ in range(6)]


def draw_board(board, current_col=None, is_human_turn=True, mode=2):
    screen.fill(DARK_BLUE)

    # Draw title
    title_text = title_font.render("CONNECT 4", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

    # Draw game board
    board_width = 7 * SQUARE_SIZE
    board_height = 6 * SQUARE_SIZE
    start_x = (WIDTH - board_width) // 2
    start_y = 150

    # Draw board background
    pygame.draw.rect(screen, BOARD_BLUE,
                     (start_x - 10, start_y - 10,
                      board_width + 20, board_height + 20),
                     border_radius=15)

    # Draw column indicators
    if current_col is not None and 0 <= current_col < 7:
        if board[0][current_col] is None:
            hover_color = YELLOW if is_human_turn else RED
            hover_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(hover_surface, hover_color + (HOVER_ALPHA,),
                               (SQUARE_SIZE // 2, SQUARE_SIZE // 2), RADIUS)
            screen.blit(hover_surface, (start_x + current_col * SQUARE_SIZE, start_y - 80))

    # Draw grid cells
    for c in range(7):
        for r in range(6):
            x = start_x + c * SQUARE_SIZE
            y = start_y + r * SQUARE_SIZE
            pygame.draw.circle(screen, BLACK, (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2), RADIUS + 3)

            piece = board[r][c]
            if piece == 'YELLOW':
                pygame.draw.circle(screen, YELLOW, (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2), RADIUS)
            elif piece == 'RED':
                pygame.draw.circle(screen, RED, (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2), RADIUS)

    pygame.display.update()


def drop_animation(board, col, is_human):
    start_x = (WIDTH - 7 * SQUARE_SIZE) // 2
    start_y = 150
    row = get_next_open_row(board, col)

    for r in range(-1, row):
        temp_y = start_y + r * SQUARE_SIZE
        draw_temp_board = [row.copy() for row in board]
        if r >= 0:
            draw_temp_board[r][col] = 'YELLOW' if is_human else 'RED'
        draw_board(draw_temp_board, None, is_human)

        # Draw falling piece
        if r < row:
            color = YELLOW if is_human else RED
            pygame.draw.circle(screen, color,
                               (start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, temp_y + SQUARE_SIZE // 2), RADIUS)

        pygame.display.update()
        pygame.time.wait(50)


def get_next_open_row(board, col):
    for r in reversed(range(6)):
        if board[r][col] is None:
            return r
    return None


def is_valid_move(board, col):
    return 0 <= col < 7 and board[0][col] is None


def check_win(board, is_human):
    piece = 'YELLOW' if is_human else 'RED'

    # Horizontal
    for r in range(6):
        for c in range(4):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Vertical
    for c in range(7):
        for r in range(3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Diagonals
    for r in range(3):
        for c in range(4):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
            if all(board[r + 3 - i][c + i] == piece for i in range(4)):
                return True
    return False


def evaluate_position(board):
    score = 0

    # Center control
    center_array = [board[i][3] for i in range(6)]
    score += center_array.count('RED') * 3

    # Horizontal
    for r in range(6):
        row = board[r]
        for c in range(4):
            window = row[c:c + 4]
            score += evaluate_window(window, 'RED', 'YELLOW')

    # Vertical
    for c in range(7):
        col = [board[r][c] for r in range(6)]
        for r in range(3):
            window = col[r:r + 4]
            score += evaluate_window(window, 'RED', 'YELLOW')

    # Diagonals
    for r in range(3):
        for c in range(4):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, 'RED', 'YELLOW')
    for r in range(3, 6):
        for c in range(4):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, 'RED', 'YELLOW')

    return score


def evaluate_window(window, player, opponent):
    score = 0
    player_count = window.count(player)
    opponent_count = window.count(opponent)
    empty = window.count(None)

    if player_count == 4:
        score += 100
    elif player_count == 3 and empty == 1:
        score += 5
    elif player_count == 2 and empty == 2:
        score += 2

    if opponent_count == 3 and empty == 1:
        score -= 4

    return score


def minimax(board, depth, alpha, beta, maximizing):
    valid_moves = [c for c in range(7) if is_valid_move(board, c)]
    is_terminal = check_win(board, False) or check_win(board, True) or not valid_moves

    if depth == 0 or is_terminal:
        if check_win(board, False):
            return (None, 100000000000000)
        elif check_win(board, True):
            return (None, -100000000000000)
        else:
            return (None, evaluate_position(board))

    if maximizing:
        value = -math.inf
        column = random.choice(valid_moves)

        for col in valid_moves:
            row = get_next_open_row(board, col)
            board_copy = [r.copy() for r in board]
            board_copy[row][col] = 'RED'
            new_score = minimax(board_copy, depth - 1, alpha, beta, False)[1]

            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_moves)

        for col in valid_moves:
            row = get_next_open_row(board, col)
            board_copy = [r.copy() for r in board]
            board_copy[row][col] = 'YELLOW'
            new_score = minimax(board_copy, depth - 1, alpha, beta, True)[1]

            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def computer_move(board):
    col, _ = minimax(board, 5, -math.inf, math.inf, True)
    return col


def show_message(text):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 200), (0, 0, WIDTH, HEIGHT))
    screen.blit(overlay, (0, 0))

    text_surf = message_font.render(text, True, WHITE)
    screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, HEIGHT // 2 - 50))

    sub_text = button_font.render("Click to continue", True, WHITE)
    screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def game_mode_screen():
    screen.fill(DARK_BLUE)

    title_text = title_font.render("SELECT MODE", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    buttons = [
        {"rect": pygame.Rect(250, 200, 400, 80), "text": "Human vs Human", "mode": 1},
        {"rect": pygame.Rect(250, 320, 400, 80), "text": "Human vs AI", "mode": 2},
        {"rect": pygame.Rect(250, 440, 400, 80), "text": "Quit", "mode": 3}
    ]

    for btn in buttons:
        pygame.draw.rect(screen, BOARD_BLUE, btn["rect"], border_radius=15)
        text = button_font.render(btn["text"], True, WHITE)
        screen.blit(text, (btn["rect"].x + 40, btn["rect"].y + 20))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn["rect"].collidepoint(x, y):
                        if btn["mode"] == 3:
                            pygame.quit()
                            sys.exit()
                        return btn["mode"]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: return 1
                if event.key == pygame.K_2: return 2
                if event.key == pygame.K_ESCAPE: return 3


def main():
    while True:
        board = create_board()
        game_over = False
        mode = game_mode_screen()

        current_col = None
        human_turn = True
        clock = pygame.time.Clock()

        while not game_over:
            if mode == 1:  # Human vs Human
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEMOTION:
                        x = pygame.mouse.get_pos()[0]
                        board_start = (WIDTH - 7 * SQUARE_SIZE) // 2
                        current_col = (
                                                  x - board_start) // SQUARE_SIZE if board_start <= x < board_start + 7 * SQUARE_SIZE else None

                    if event.type == pygame.MOUSEBUTTONDOWN and current_col is not None:
                        if is_valid_move(board, current_col):
                            # Play animation
                            drop_animation(board, current_col, human_turn)

                            # Update actual board state after animation
                            row = get_next_open_row(board, current_col)
                            board[row][current_col] = 'YELLOW' if human_turn else 'RED'

                            # Show final board state
                            draw_board(board, None, human_turn, mode)
                            pygame.display.update()

                            # Add slight delay before win check
                            pygame.time.wait(100)

                            if check_win(board, human_turn):
                                winner = "Yellow Player Wins!" if human_turn else "Red Player Wins!"
                                show_message(winner)
                                game_over = True
                            elif all(all(cell is not None for cell in row) for row in board):
                                show_message("Draw!")
                                game_over = True
                            else:
                                human_turn = not human_turn

            elif mode == 2:  # Human vs AI
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if human_turn:
                        if event.type == pygame.MOUSEMOTION:
                            x = pygame.mouse.get_pos()[0]
                            board_start = (WIDTH - 7 * SQUARE_SIZE) // 2
                            current_col = (
                                                      x - board_start) // SQUARE_SIZE if board_start <= x < board_start + 7 * SQUARE_SIZE else None

                        if event.type == pygame.MOUSEBUTTONDOWN and current_col is not None:
                            if is_valid_move(board, current_col):
                                # Human move animation
                                drop_animation(board, current_col, True)

                                # Update board after animation
                                row = get_next_open_row(board, current_col)
                                board[row][current_col] = 'YELLOW'

                                # Show final state
                                draw_board(board, None, False, mode)
                                pygame.display.update()
                                pygame.time.wait(100)

                                if check_win(board, True):
                                    show_message("You Win!")
                                    game_over = True
                                elif all(all(cell is not None for cell in row) for row in board):
                                    show_message("Draw!")
                                    game_over = True
                                else:
                                    human_turn = False  # Switch to AI turn

                # AI move handling
                if not human_turn and not game_over:
                    # Show AI thinking
                    draw_board(board, None, False, mode)
                    pygame.display.update()
                    pygame.time.wait(500)

                    # Get AI move
                    col = computer_move(board)

                    if col is not None and is_valid_move(board, col):
                        # AI move animation
                        drop_animation(board, col, False)

                        # Update board after animation
                        row = get_next_open_row(board, col)
                        board[row][col] = 'RED'

                        # Show final state
                        draw_board(board, None, True, mode)
                        pygame.display.update()
                        pygame.time.wait(100)

                        if check_win(board, False):
                            show_message("AI Wins!")
                            game_over = True
                        elif all(all(cell is not None for cell in row) for row in board):
                            show_message("Draw!")
                            game_over = True
                        else:
                            human_turn = True  # Switch back to human

            draw_board(board, current_col, human_turn, mode)
            clock.tick(FPS)

        # Reset after game over
        main()


if __name__ == "__main__":
    main()