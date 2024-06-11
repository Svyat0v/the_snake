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

    def __init__(self, bg_color=BOARD_BACKGROUND_COLOR,
                 position=CENTER_SCREEN):
        self.position = position
        self.body_color = bg_color

    def draw_cell(self, position):
        """Создание ячейки."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def remove_cell(self, position):
        """Метод remove_cell подтирание последнего сигмента."""
        last_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def draw(self):
        """Отрисовка объекта. По умолчанию pass."""
        pass


class Apple(GameObject):
    """Класс для яблока, наследуется от GameObject."""

    def __init__(self, bg_color=APPLE_COLOR):
        """Инициализация яблока."""
        super().__init__(bg_color)
        self.randomize_position([CENTER_SCREEN])

    def randomize_position(self, danger_zone):
        """Реализация рандомного появления яблока."""
        x_pos = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y_pos = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x_pos, y_pos)
        while self.position in danger_zone:
            self.randomize_position(danger_zone)

    def draw(self):
        """Метод draw класса Apple."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс для змейки, наследуется от GameObject."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация змейки с заданными позицией и цветом."""
        super().__init__(body_color)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)

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
        x_direction, y_direction = self.direction
        x_new = (GRID_SIZE * x_direction + head_x) % SCREEN_WIDTH
        y_new = (GRID_SIZE * y_direction + head_y) % SCREEN_HEIGHT

        self.positions.insert(0, (x_new, y_new))
        if len(self.positions) > self.length:
            last = self.positions.pop()
            self.remove_cell(last)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def draw(self):
        """Метод draw класса Snake,отрисовка головы."""
        for position in self.positions:
            self.draw_cell(position)


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
    game_object.update_direction()


def main():
    """Создаем экземпляры классов"""
    pygame.init()

    apple = Apple()
    snake = Snake()

    apple.draw()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if (snake.get_head_position() in snake.positions[2:])\
                or snake.length == (GRID_WIDTH * GRID_HEIGHT):
            snake.reset()
            apple.randomize_position(snake.positions)
            apple.draw()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
            apple.draw()

        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
