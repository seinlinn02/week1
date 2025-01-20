import pygame
from game_design import GameDesign
from game_functions import initialize_game, show_game_over_screen


def main():
    try:
        # Initialize game components
        screen, WINDOW_SIZE, HEADER_HEIGHT, GRID_SIZE, GRID_COUNT, PLAY_AREA_SIZE = initialize_game()

        # Create game instance
        game = GameDesign(GRID_COUNT, GRID_SIZE, HEADER_HEIGHT)
        clock = pygame.time.Clock()

        # Game state
        running = True
        while running:
            if game.game_over:
                show_game_over_screen(screen, game.score, game.high_score, WINDOW_SIZE)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game.reset_game()
                        elif event.key == pygame.K_ESCAPE:
                            running = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            game.snake.change_direction([0, -1])
                        elif event.key == pygame.K_DOWN:
                            game.snake.change_direction([0, 1])
                        elif event.key == pygame.K_LEFT:
                            game.snake.change_direction([-1, 0])
                        elif event.key == pygame.K_RIGHT:
                            game.snake.change_direction([1, 0])
                        elif event.key == pygame.K_ESCAPE:
                            running = False

                # Update game state
                game.update()

                # If game over after update, continue to next iteration
                if game.game_over:
                    continue

                # Draw game
                game.draw(screen, WINDOW_SIZE)
                pygame.display.flip()
                clock.tick(10)  # Control game speed

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Quitting game...")
        pygame.quit()
        print("Game quit successfully")


if __name__ == "__main__":
    main()