import pygame
import random


class Snake:
    def __init__(self, GRID_COUNT):
        self.GRID_COUNT = GRID_COUNT
        self.reset()

    def reset(self):
        self.body = [(self.GRID_COUNT // 2, self.GRID_COUNT // 2)]
        self.direction = [1, 0]  # Start moving right
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (
            head[0] + self.direction[0],
            head[1] + self.direction[1]
        )

        if new_head in self.body or not (0 <= new_head[0] < self.GRID_COUNT and 0 <= new_head[1] < self.GRID_COUNT):
            return False  # Game over        

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True

    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        if (new_direction[0] != -self.direction[0] or
                new_direction[1] != -self.direction[1]):
            self.direction = new_direction


class Food:
    def __init__(self, snake_body, GRID_COUNT):
        self.GRID_COUNT = GRID_COUNT
        self.position = self.generate_position(snake_body)

    def generate_position(self, snake_body):
        while True:
            position = (
                random.randint(0, self.GRID_COUNT - 1),
                random.randint(0, self.GRID_COUNT - 1)
            )
            if position not in snake_body:
                return position


class GameDesign:
    def __init__(self, GRID_COUNT, GRID_SIZE, HEADER_HEIGHT):
        self.GRID_COUNT = GRID_COUNT
        self.GRID_SIZE = GRID_SIZE
        self.HEADER_HEIGHT = HEADER_HEIGHT
        self.snake = Snake(GRID_COUNT)
        self.food = Food(self.snake.body, GRID_COUNT)
        self.game_over = False
        self.score = 0
        self.high_score = 0

        # Colors
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (50, 50, 50)
        self.WHITE = (255, 255, 255)

    def reset_game(self):
        self.snake.reset()
        self.food = Food(self.snake.body, self.GRID_COUNT)
        self.game_over = False
        self.score = 0

    def update(self):
        if not self.snake.move():
            self.score = len(self.snake.body) - 1
            self.high_score = max(self.high_score, self.score)
            self.game_over = True
            return

        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            self.food = Food(self.snake.body, self.GRID_COUNT)
            self.score = len(self.snake.body) - 1

    def draw_header(self, screen, WINDOW_SIZE):
        # Draw header background
        header_rect = pygame.Rect(0, 0, WINDOW_SIZE, self.HEADER_HEIGHT)
        pygame.draw.rect(screen, self.GRAY, header_rect)

        # Draw dividing line
        pygame.draw.line(screen, self.WHITE,
                         (WINDOW_SIZE // 2, 5),
                         (WINDOW_SIZE // 2, self.HEADER_HEIGHT - 5), 2)

        font = pygame.font.Font(None, 36)
        # Draw score on left
        score_text = font.render(f"Score: {self.score}", True, self.WHITE)
        score_rect = score_text.get_rect(midtop=(WINDOW_SIZE // 4, 15))
        screen.blit(score_text, score_rect)

        # Draw high score on right
        high_score_text = font.render(f"High Score: {self.high_score}", True, self.WHITE)
        high_score_rect = high_score_text.get_rect(midtop=(WINDOW_SIZE * 3 // 4, 15))
        screen.blit(high_score_text, high_score_rect)

    def draw(self, screen, WINDOW_SIZE):
        # Clear screen
        screen.fill(self.BLACK)

        # Draw header
        self.draw_header(screen, WINDOW_SIZE)

        # Draw snake
        for segment in self.snake.body:
            pygame.draw.rect(screen, self.GREEN, (
                segment[0] * self.GRID_SIZE,
                segment[1] * self.GRID_SIZE + self.HEADER_HEIGHT,
                self.GRID_SIZE - 1,
                self.GRID_SIZE - 1
            ))

        # Draw food
        pygame.draw.rect(screen, self.RED, (
            self.food.position[0] * self.GRID_SIZE,
            self.food.position[1] * self.GRID_SIZE + self.HEADER_HEIGHT,
            self.GRID_SIZE - 1,
            self.GRID_SIZE - 1
        ))