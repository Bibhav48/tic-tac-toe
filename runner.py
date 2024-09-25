import pygame
import sys
import time
import cv2
import numpy as np
import dotenv
import os

import tictactoe as ttt

# Load environment variables
dotenv.load_dotenv()

# Initialize pygame
pygame.init()
size = width, height = 600, 400

# Ensure media folder exists
if not os.path.exists('media'):
    os.makedirs('media')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game state
games = int(os.getenv("GAMES", "0")) + 1
user = None
board = ttt.initial_state()
ai_turn = False
game_over = False
blunder_detected = False

# Global variable for tiles
tiles = None

# Recording state
recording = False
out = None

# FPS settings
GAME_FPS = 60
VIDEO_FPS = 30

# Initialize pygame window and clock
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Load fonts
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)


def start_recording():
    global recording, out
    if not recording:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(
            f'media/game_{games}.mp4', fourcc, VIDEO_FPS, (width, height))
        recording = True


def stop_recording():
    global recording, out
    if recording:
        out.release()
        recording = False


def reset_game():
    global user, board, ai_turn, game_over, blunder_detected, games, tiles
    user = None
    board = ttt.initial_state()
    ai_turn = False
    game_over = False
    blunder_detected = False
    tiles = None  # Reset tiles on new game
    games += 1
    stop_recording()


def draw_board():
    global tiles
    tile_size = 80
    tile_origin = (width / 2 - (1.5 * tile_size),
                   height / 2 - (1.5 * tile_size))
    tiles = []
    for i in range(3):
        row = []
        for j in range(3):
            rect = pygame.Rect(
                tile_origin[0] + j * tile_size,
                tile_origin[1] + i * tile_size,
                tile_size, tile_size
            )
            pygame.draw.rect(screen, WHITE, rect, 3)

            if board[i][j] != ttt.EMPTY:
                move = moveFont.render(board[i][j], True, WHITE)
                moveRect = move.get_rect()
                moveRect.center = rect.center
                screen.blit(move, moveRect)
            row.append(rect)
        tiles.append(row)


def draw_title(text):
    title = largeFont.render(text, True, WHITE)
    titleRect = title.get_rect()
    titleRect.center = ((width / 2), 30)
    screen.blit(title, titleRect)


def draw_button(text, rect):
    button = pygame.draw.rect(screen, WHITE, rect)
    buttonText = mediumFont.render(text, True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = button.center
    screen.blit(buttonText, buttonRect)
    return button


def handle_events():
    global user, board, ai_turn, game_over, blunder_detected
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop_recording()
            with open(".env", "w") as f:
                f.write(f"GAMES={games}\n")
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if user is None:
                if playXButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = ttt.X
                    start_recording()
                elif playOButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = ttt.O
                    start_recording()
            elif game_over:
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    reset_game()
            elif user == ttt.player(board):
                for i in range(3):
                    for j in range(3):
                        # Check if tiles exists
                        if tiles and board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse):
                            board = ttt.result(board, (i, j))

                            # Redraw board to include the move before capturing the blunder
                            draw_board()
                            pygame.display.flip()

                            # Check for blunders
                            check_best = ttt.review(board)
                            if check_best['val'] != 0 and not blunder_detected:
                                print("Blunder!!")
                                blunder_detected = True
                                pygame.draw.rect(screen, RED, tiles[i][j], 3)
                                pygame.display.flip()  # Ensure the red rectangle is drawn
                                pygame.image.save(
                                    screen, f"media/Blunder_game{games}.jpeg")
                                pygame.draw.rect(screen, WHITE, tiles[i][j], 3)
                                pygame.display.flip()  # Redraw the white border


def check_game_over():
    global game_over
    if ttt.terminal(board):
        game_over = True
        winner = ttt.winner(board)
        if winner is None:
            return "Game Over: Tie."
        else:
            return f"Game Over: {winner} wins."
    return None


def ai_move():
    global board, ai_turn
    if ai_turn:
        move = ttt.minimax(board)
        board = ttt.result(board, move)
        ai_turn = False
    else:
        ai_turn = True


# Main game loop
while True:
    screen.fill(BLACK)

    if user is None:
        draw_title("Play Tic-Tac-Toe")
        playXButton = draw_button("Play as X", pygame.Rect(
            (width / 8), (height / 2), width / 4, 50))
        playOButton = draw_button("Play as O", pygame.Rect(
            5 * (width / 8), (height / 2), width / 4, 50))
    else:
        draw_board()  # Ensure tiles are always defined when drawing the board
        game_over_message = check_game_over()

        if game_over_message:
            draw_title(game_over_message)
            againButton = draw_button("Play Again", pygame.Rect(
                width / 3, height - 65, width / 3, 50))
        elif user == ttt.player(board):
            draw_title(f"Play as {user}")
        else:
            draw_title("Computer thinking...")
            ai_move()

    handle_events()

    pygame.display.flip()

    if recording:
        screen_data = pygame.surfarray.array3d(screen)
        screen_rgb = np.swapaxes(screen_data, 0, 1)
        out.write(screen_rgb)

    clock.tick(GAME_FPS)
