import pygame


def initialize_game():
    print("Initializing Pygame...")
    pygame.init()
    print("Pygame initialized successfully")

    # Constants
    WINDOW_SIZE = 600
    HEADER_HEIGHT = 60
    GRID_SIZE = 20
    PLAY_AREA_SIZE = WINDOW_SIZE - HEADER_HEIGHT
    GRID_COUNT = PLAY_AREA_SIZE // GRID_SIZE

    print(f"Setting up display with window size: {WINDOW_SIZE}x{WINDOW_SIZE}")
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Snake Game")
    print("Display set up successfully")

    return screen, WINDOW_SIZE, HEADER_HEIGHT, GRID_SIZE, GRID_COUNT, PLAY_AREA_SIZE


def draw_text(screen, text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def show_game_over_screen(screen, score, high_score, WINDOW_SIZE):
    screen.fill((0, 0, 0))
    draw_text(screen, "GAME OVER!", 64, WINDOW_SIZE // 2, WINDOW_SIZE // 4, (255, 0, 0))
    draw_text(screen, f"Score: {score}", 36, WINDOW_SIZE // 2, WINDOW_SIZE // 2, (255, 255, 255))
    draw_text(screen, f"High Score: {high_score}", 36, WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 40, (255, 255, 255))
    draw_text(screen, "Press SPACE to Play Again or ESC to Quit", 24, WINDOW_SIZE // 2, WINDOW_SIZE * 3 // 4,
              (255, 255, 255))
    pygame.display.flip()