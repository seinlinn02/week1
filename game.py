import pygame
import time
import random
from enum import Enum

# Initialize pygame
pygame.init()

# Define colors as an enumeration
class Colors(Enum):
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 102)
    BLACK = (0, 0, 0)
    RED = (213, 50, 80)
    GREEN = (0, 255, 0)
    BLUE = (50, 153, 213)
    PURPLE = (128, 0, 128)  # For power-ups

# Game configuration
class GameConfig:
    DIS_WIDTH = 800
    DIS_HEIGHT = 600
    SNAKE_BLOCK = 10
    HIGH_SCORE_FILE = "high_score.txt"
    FPS = {
        "EASY": 10,
        "MEDIUM": 15,
        "HARD": 20
    }

class PowerUp:
    def __init__(self):
        self.active = False
        self.position = (0, 0)
        self.type = None
        self.duration = 0
        self.start_time = 0

    def spawn(self, game_width, game_height, block_size):
        self.position = (
            round(random.randrange(0, game_width - block_size) / 10.0) * 10.0,
            round(random.randrange(0, game_height - block_size) / 10.0) * 10.0
        )
        self.active = True
        self.type = random.choice(["SPEED", "SLOW", "DOUBLE_SCORE"])
        self.duration = 5  # Duration in seconds
        self.start_time = time.time()

    def is_expired(self):
        return time.time() - self.start_time > self.duration if self.active else False

class SnakeGame:
    def __init__(self):
        self.display = pygame.display.set_mode((GameConfig.DIS_WIDTH, GameConfig.DIS_HEIGHT))
        pygame.display.set_caption('Enhanced Snake Game')
        self.clock = pygame.time.Clock()
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        self.high_score = self.load_high_score()
        self.power_up = PowerUp()
        self.current_speed = 0
        self.score_multiplier = 1

    def load_high_score(self):
        try:
            with open(GameConfig.HIGH_SCORE_FILE, "r") as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self, score):
        try:
            with open(GameConfig.HIGH_SCORE_FILE, "w") as file:
                file.write(str(score))
        except Exception as e:
            print(f"Error saving high score: {e}")

    def display_score(self, score):
        value = self.score_font.render(f"Score: {score}", True, Colors.YELLOW.value)
        self.display.blit(value, [0, 0])
        high_score = self.score_font.render(f"High Score: {self.high_score}", True, Colors.YELLOW.value)
        self.display.blit(high_score, [0, 40])

    def draw_snake(self, snake_list):
        for segment in snake_list:
            pygame.draw.rect(self.display, Colors.BLACK.value, 
                           [segment[0], segment[1], GameConfig.SNAKE_BLOCK, GameConfig.SNAKE_BLOCK])

    def show_message(self, msg, color):
        message = self.font_style.render(msg, True, color)
        self.display.blit(message, [GameConfig.DIS_WIDTH / 6, GameConfig.DIS_HEIGHT / 3])

    def choose_difficulty(self):
        self.display.fill(Colors.BLUE.value)
        self.show_message("Choose Difficulty: 1-Easy, 2-Medium, 3-Hard", Colors.WHITE.value)
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return GameConfig.FPS["EASY"]
                    elif event.key == pygame.K_2:
                        return GameConfig.FPS["MEDIUM"]
                    elif event.key == pygame.K_3:
                        return GameConfig.FPS["HARD"]

    def handle_power_up(self, snake_head):
        if self.power_up.active:
            if self.power_up.is_expired():
                self.power_up.active = False
                self.current_speed = self.base_speed
                self.score_multiplier = 1
            elif snake_head == list(self.power_up.position):
                if self.power_up.type == "SPEED":
                    self.current_speed = min(self.base_speed * 1.5, 30)
                elif self.power_up.type == "SLOW":
                    self.current_speed = max(self.base_speed * 0.5, 5)
                elif self.power_up.type == "DOUBLE_SCORE":
                    self.score_multiplier = 2
                self.power_up.active = False

    def gameLoop(self):
        game_over = False
        game_close = False

        x1 = GameConfig.DIS_WIDTH / 2
        y1 = GameConfig.DIS_HEIGHT / 2
        x1_change = 0
        y1_change = 0

        snake_list = []
        length_of_snake = 1

        foodx = round(random.randrange(0, GameConfig.DIS_WIDTH - GameConfig.SNAKE_BLOCK) / 10.0) * 10.0
        foody = round(random.randrange(0, GameConfig.DIS_HEIGHT - GameConfig.SNAKE_BLOCK) / 10.0) * 10.0

        self.base_speed = self.choose_difficulty()
        self.current_speed = self.base_speed

        # Add pause functionality
        paused = False

        while not game_over:
            while game_close:
                self.display.fill(Colors.BLUE.value)
                self.show_message("Game Over! Q-Quit or C-Play Again", Colors.RED.value)
                self.display_score((length_of_snake - 1) * self.score_multiplier)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            self.gameLoop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Pause game
                        paused = not paused
                    if not paused:
                        # Arrow keys
                        if event.key in (pygame.K_LEFT, pygame.K_a) and x1_change == 0:
                            x1_change = -GameConfig.SNAKE_BLOCK
                            y1_change = 0
                        elif event.key in (pygame.K_RIGHT, pygame.K_d) and x1_change == 0:
                            x1_change = GameConfig.SNAKE_BLOCK
                            y1_change = 0
                        elif event.key in (pygame.K_UP, pygame.K_w) and y1_change == 0:
                            y1_change = -GameConfig.SNAKE_BLOCK
                            x1_change = 0
                        elif event.key in (pygame.K_DOWN, pygame.K_s) and y1_change == 0:
                            y1_change = GameConfig.SNAKE_BLOCK
                            x1_change = 0

            if paused:
                self.show_message("PAUSED - Press P to continue", Colors.WHITE.value)
                pygame.display.update()
                continue

            # Check for wall collision with portal effect
            if x1 >= GameConfig.DIS_WIDTH:
                x1 = 0
            elif x1 < 0:
                x1 = GameConfig.DIS_WIDTH - GameConfig.SNAKE_BLOCK
            elif y1 >= GameConfig.DIS_HEIGHT:
                y1 = 0
            elif y1 < 0:
                y1 = GameConfig.DIS_HEIGHT - GameConfig.SNAKE_BLOCK

            x1 += x1_change
            y1 += y1_change
            self.display.fill(Colors.BLUE.value)
            
            # Draw food
            pygame.draw.rect(self.display, Colors.GREEN.value, 
                           [foodx, foody, GameConfig.SNAKE_BLOCK, GameConfig.SNAKE_BLOCK])

            # Draw power-up if active
            if self.power_up.active and not self.power_up.is_expired():
                pygame.draw.rect(self.display, Colors.PURPLE.value,
                               [self.power_up.position[0], self.power_up.position[1], 
                                GameConfig.SNAKE_BLOCK, GameConfig.SNAKE_BLOCK])

            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            # Check for self collision
            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_close = True

            self.draw_snake(snake_list)
            self.display_score((length_of_snake - 1) * self.score_multiplier)
            
            # Handle power-ups
            self.handle_power_up(snake_head)

            pygame.display.update()

            # Food collision
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, GameConfig.DIS_WIDTH - GameConfig.SNAKE_BLOCK) / 10.0) * 10.0
                foody = round(random.randrange(0, GameConfig.DIS_HEIGHT - GameConfig.SNAKE_BLOCK) / 10.0) * 10.0
                length_of_snake += 1

                # Spawn power-up with 20% chance
                if random.random() < 0.2 and not self.power_up.active:
                    self.power_up.spawn(GameConfig.DIS_WIDTH, GameConfig.DIS_HEIGHT, GameConfig.SNAKE_BLOCK)

                # Update high score
                current_score = (length_of_snake - 1) * self.score_multiplier
                if current_score > self.high_score:
                    self.high_score = current_score
                    self.save_high_score(self.high_score)

            self.clock.tick(self.current_speed)

        pygame.quit()
        quit()

# Start the game
if __name__ == "__main__":
    game = SnakeGame()
    game.gameLoop()