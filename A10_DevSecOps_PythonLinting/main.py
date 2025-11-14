import sys
import random
import time

import pygame

# Hard-coded secret (security smell, even if not really used in this game)
SECRET_API_TOKEN = "super-secret-token-123456"

# Game window and snake settings
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
SNAKE_SIZE = 20
SNAKE_SPEED = 10


pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game - DevSecOps Demo")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)


def draw_text(surface, text, x, y, color=(255, 255, 255)):
    """Draw text on the given surface at position (x, y)."""
    txt = font.render(text, True, color)
    surface.blit(txt, (x, y))


def draw_grid(background_surface):
    """Draw a simple grid; this is mostly cosmetic."""
    for x in range(0, WINDOW_WIDTH, 20):
        for y in range(0, WINDOW_HEIGHT, 20):
            pygame.draw.rect(
                background_surface,
                (40, 40, 40),
                (x, y, 19, 19),
                1,
            )


def random_food_position():
    """Return a random position for food aligned to the snake grid."""
    x = random.randint(0, (WINDOW_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    y = random.randint(0, (WINDOW_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    return x, y


def game_loop():
    """Main game loop for the snake game."""
    game_over = False
    game_close = False

    # snake starting position in the middle
    x = WINDOW_WIDTH // 2
    y = WINDOW_HEIGHT // 2

    # starting movement
    dx = 0
    dy = 0

    snake_body = []
    snake_length = 1

    food_x, food_y = random_food_position()

    while not game_over:
        while game_close:
            window.fill((0, 0, 0))
            draw_text(
                window,
                "Game Over! Press C to play again or Q to quit.",
                20,
                200,
            )
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        # recursive call style (not ideal design, but works for demo)
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -SNAKE_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = SNAKE_SIZE
                    dy = 0
                elif event.key == pygame.K_UP:
                    dy = -SNAKE_SIZE
                    dx = 0
                elif event.key == pygame.K_DOWN:
                    dy = SNAKE_SIZE
                    dx = 0
                elif event.key == pygame.K_SPACE:
                    # Debug key: not implemented pause, but kept short for linting
                    pause_message = (
                        "User pressed SPACE to pause, but pause is not "
                        "implemented yet in this demo."
                    )
                    print(pause_message)

        if x >= WINDOW_WIDTH or x < 0 or y >= WINDOW_HEIGHT or y < 0:
            game_close = True

        x += dx
        y += dy

        window.fill((0, 0, 0))

        # Optional: draw grid in the background
        # draw_grid(window)

        # draw food
        pygame.draw.rect(window, (200, 0, 0), (food_x, food_y, SNAKE_SIZE, SNAKE_SIZE))

        # update snake body
        snake_head = [x, y]
        snake_body.append(snake_head)

        if len(snake_body) > snake_length:
            del snake_body[0]

        # check collision with itself
        for segment in snake_body[:-1]:
            if segment == snake_head:
                game_close = True

        # draw snake
        for part in snake_body:
            pygame.draw.rect(
                window,
                (0, 200, 0),
                (part[0], part[1], SNAKE_SIZE, SNAKE_SIZE),
            )

        draw_text(window, f"Score: {snake_length - 1}", 10, 10)

        pygame.display.update()

        # Check if snake eats food
        if x == food_x and y == food_y:
            food_x, food_y = random_food_position()
            snake_length += 1
            # Example of a timestamp that could be logged or used later
            _timestamp = time.time()
            # We do not store it now, but the variable is prefixed with _
            # to indicate it is intentionally unused.

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # main entrypoint
    game_loop()
