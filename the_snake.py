import pygame

from random import choice, randint

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Центр экранна:
CENTER_SCREEN = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)


class GameObject:
    """Это базовый класс."""

    def __init__(self, bg_color=BOARD_BACKGROUND_COLOR):
        self.position = CENTER_SCREEN
        self.body_color = bg_color

    def draw(self):
        """Отрисовка объекта. По умолчанию pass."""
        pass


class Apple(GameObject):
    """Класс для яблока, наследуется от GameObject."""

    def __init__(self, bg_color=APPLE_COLOR):
        """Инициализация яблока."""
        super().__init__(bg_color)
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """Реализация рандомного появления яблока."""
        x_pos = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y_pos = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        if (x_pos, y_pos) == snake_positions == CENTER_SCREEN:
            x_pos = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_pos = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x_pos, y_pos)

    def draw(self):
        """Метод draw класса Apple. (Взято из прекода)"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки, наследуется от GameObject."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация змейки с заданными позицией и цветом."""
        super().__init__(body_color)
        self.reset()
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.position = CENTER_SCREEN
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляем позицию змейки.
        Управление её движением по игровому полю.
        """
        head_x, head_y = self.get_head_position()
        xd, yd = self.direction
        x_new = (GRID_SIZE * xd + head_x) % SCREEN_WIDTH
        y_new = (GRID_SIZE * yd + head_y) % SCREEN_HEIGHT

        self.positions.insert(0, (x_new, y_new))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def draw(self):
        """Метод draw класса Snake. (Взято из прекода)"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Создаем экземпляры классов"""
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.draw()
            apple.randomize_position(snake.positions)

        pygame.display.update()


if __name__ == '__main__':
    main()
