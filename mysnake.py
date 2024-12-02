import pygame as pg
import pygame_menu
from random import choice, randint
from pygame import K_ESCAPE

SCREEN_WIDTH, SCREEN_HEIGHT = 840, 480
GRID_SIZE = 20
AREA_WIDTH = (0, 640)
AREA_HEIGHT = (0, 480)
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT // GRID_SIZE)
CENTER_POINT = ((AREA_WIDTH[1] // 2), (AREA_HEIGHT[1] // 2))
BOARD_BACKGROUND_COLOR = (170, 215, 81)
SNAKE_COLOR = (225, 242, 29)
APPLE_COLOR = (255, 0, 0)
GOLD_APPLE = (255, 255, 0)
ORANGE = (255, 150, 0)
PLUM = (150, 0, 255)

# Направления движения.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# Позиция за границами игрового поля. Оттуда дергаем наши объекты,
# а после поедания возвращаем обратно. Пробовал с просто удалять позицию
# через del, но так мы полностью избавляемся от аттрибута.
ob_position = [(SCREEN_WIDTH + 20, SCREEN_HEIGHT)]
draw_position = [(x, y) for x in range(AREA_WIDTH[0], AREA_WIDTH[1], 60)
                        for y in range(AREA_HEIGHT[0], AREA_HEIGHT[1], 60)]
occupied_cell = []

# Настройка игрового окна.
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени.
clock = pg.time.Clock()

images = {
    'fon' : pg.image.load('fon.png.'),
    'frame' : pg.image.load('frame.png.'),
    'logo' : pg.image.load('logo.png.'),
    'logo_menu' : pg.image.load('logo_2.png.'),
    'wall_level_2' : pg.image.load('wall_level_2.png.'),
    'wall_level_3' : pg.image.load('wall_level_3.png.')
}

def handle_keys(game_object):
    """Обрабатывает нажатие клавиш"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if ((event.key == pg.K_UP or event.key == pg.K_w)
                    and game_object.direction != DOWN):
                game_object.next_direction = UP
            elif ((event.key == pg.K_DOWN or event.key == pg.K_s)
                  and game_object.direction != UP):
                game_object.next_direction = DOWN
            elif ((event.key == pg.K_LEFT or event.key == pg.K_a)
                  and game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif ((event.key == pg.K_RIGHT or event.key == pg.K_d)
                  and game_object.direction != LEFT):
                game_object.next_direction = RIGHT
            elif event.key == K_ESCAPE:
                # ESC key pressed
                pg.quit()
                raise SystemExit

class GameObject:
    """Общее описание объектов игры."""

    def __init__(self, bady_color=None) -> None:
        """Инициализирует базовые атрибуты объекта."""
        self.position = ((40, 40))
        self.body_color = bady_color

    def randomize_position(self):
        """Устанавливает случайное положение яблока."""
        self.position = choice(draw_position)

    def draw(self, position):
        """Метод для переопределения в дочерних классах"""

    def draw_cell(self, position):
        """Отрисовка клетки."""
        cell = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, cell)

class Snake(GameObject):
    """Описание змейки"""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__( bady_color=SNAKE_COLOR)
        self.length = 1
        self.score = 0
        self.speed = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        self.update_direction()
        # Записываем последнюю позицию змейки для последующего затирания.
        # Обновляем координаты головы. % позволяет перемещаться сквозь стены.
        new_positions = ((self.get_head_position()[0] + self.direction[0]
                          * GRID_SIZE) % AREA_WIDTH[1],
                         (self.get_head_position()[1] + self.direction[1]
                          * GRID_SIZE) % AREA_HEIGHT[1])
        # Обработка столкновения со своим телом.
        if new_positions in self.positions:
            self.reset()
        else:
            self.positions.insert(0, new_positions)
            # Затирание хвоста следа.
            if len(self.positions) > self.length:
                self.positions.pop()
    def move_leve_2(self):
        """Обновляет позицию змейки."""
        self.update_direction()
        # Записываем последнюю позицию змейки для последующего затирания.
        self.last = self.positions[-1]
        # Обновляем координаты головы. % позволяет перемещаться сквозь стены.
        new_positions = (self.get_head_position()[0] + self.direction[0]
                              * GRID_SIZE,
                              self.get_head_position()[1] + self.direction[1]
                              * GRID_SIZE)
        x, y = new_positions
        # Обработка столкновения со своим телом.
        if new_positions in self.positions or ((x == 620) or (x == 0) or (y == 460) or (y == 0)):
            self.reset()
        else:
            self.positions.insert(0, new_positions)
            # Затирание хвоста следа.
            if len(self.positions) > self.length:
                self.positions.pop()
            self.draw()

    def move_leve_3(self):
        """Обновляет позицию змейки."""
        self.update_direction()
        # Записываем последнюю позицию змейки для последующего затирания.
        self.last = self.positions[-1]
        # Обновляем координаты головы. % позволяет перемещаться сквозь стены.
        new_positions = ((self.get_head_position()[0] + self.direction[0]
                          * GRID_SIZE) % AREA_WIDTH[1],
                         (self.get_head_position()[1] + self.direction[1]
                          * GRID_SIZE) % AREA_HEIGHT[1])
        x, y = new_positions
        # Обработка столкновения со своим телом.
        if new_positions in self.positions or (x == 320 or y == 240 or x == 300 or y == 220):
            self.reset()
        else:
            self.positions.insert(0, new_positions)
            # Затирание хвоста следа.
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след"""
        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)

        # Отрисовка головы змейки.
        self.draw_cell(self.positions[0])

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.length = 1
        self.score = 0
        AREA_WIDTH = (0, 640)
        AREA_HEIGHT = (0, 480)
        self.positions = [self.position]
        # Очищает игровое поле после столкновения.

class Apple(GameObject):
    """Описание яблока"""

    def __init__(self):
        """Задаёт цвет и позицию яблока."""
        super().__init__(bady_color=APPLE_COLOR)
        self.randomize_position()

    def draw(self):
        """Отрисовывает объекта на игровом поле."""
        self.draw_cell(self.position)

class Gold(GameObject):
    """Описание апельсина(бонус к очкам)"""

    def __init__(self):
        """Задаёт цвет и позицию яблока."""
        super().__init__()
        self.body_color = GOLD_APPLE
        self.position = ob_position

    def draw(self):
        """Отрисовывает объекта на игровом поле."""
        self.draw_cell(self.position)

    def del_position(self):
        self.position = ob_position

class Orange(GameObject):
    """Описание апельсина(уменьшение длины)"""
    def __init__(self):
        """Задаёт цвет и позицию яблока."""
        super().__init__()
        self.body_color = ORANGE
        self.position = ob_position

    def draw(self):
        """Отрисовывает объекта на игровом поле."""
        self.draw_cell(self.position)

    def del_position(self):
        self.position = ob_position

class Plum(GameObject):
    """Описание сливы(уменьшение скорости)"""
    def __init__(self):
        """Задаёт цвет и позицию яблока."""
        super().__init__()
        self.body_color = PLUM
        self.position = ob_position

    def draw(self):
        """Отрисовывает объекта на игровом поле."""
        self.draw_cell(self.position)

    def del_position(self):
        self.position = ob_position

def main():
    """Запуск игры"""
    # Создание поверхности для игры.
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pg.display.set_caption('Изгиб питона')
    font = pg.font.SysFont('comicsans', 27)
    timer_duration = 10000
    timer_level_font = 5000
    timer = 0
    gold = Gold()
    orange = Orange()
    plum = Plum()
    snake = Snake()
    apple = Apple()
    level = 1
    flag = True
    ob = None
    global AREA_WIDTH
    global AREA_HEIGHT
    best_score = 0
    cont = 0

    while True:
        # Настройка скорости змейки.
        speed = snake.speed + snake.length // 10 - cont
        clock.tick(5 + speed)
        if best_score < snake.score:
            best_score = snake.score
        # Активация управления.
        handle_keys(snake)
        screen.fill(BOARD_BACKGROUND_COLOR)
        screen.blit(images['fon'], (0, 0))
        screen.blit(images['frame'], (640, 0))
        screen.blit(images['logo'], (655, 20))
        apple.draw()
        if 1000 > snake.score >= 500:
            AREA_WIDTH = (20, 620)
            AREA_HEIGHT = (20, 460)
            if level == 1:
                level += 1
                apple.randomize_position()
            screen.blit(images['wall_level_2'], (0, 0))
            snake.move_leve_2()

        elif snake.score >= 1000:
            AREA_WIDTH = (0, 640)
            AREA_HEIGHT = (0, 480)
            step = 40
            if level == 1:
                level += 1
                apple.randomize_position()
            screen.blit(images['wall_level_3'], (0, 0))
            snake.move_leve_3()
        else:
            snake.move()

        # Обработка события поедания яблока.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.score += 10
            apple.randomize_position()
        while apple.position in snake.positions:
            apple.randomize_position()

        if flag and 1 == randint(1, 100):
            ob = choice([gold, plum, orange])
            ob.randomize_position()
            while ob.position in snake.positions:
                ob.randomize_position()  # Случайная позиция для gold
            timer = pg.time.get_ticks()  # Запоминаем время появления
            flag = False

        # Если позиция записана, то отображаем
        if ob and ob.position != ob_position:
            ob.draw()
        # Удаляем gold после 10 секунд
            if not flag and pg.time.get_ticks() - timer >= timer_duration:
                ob.position = ob_position
                flag = True
        # Удаляем gold при его поедании
            elif snake.get_head_position() == gold.position:
                gold.position = ob_position
                flag = True
                snake.score += 100
                snake.length += 1
        # Удаляем gold при его поедании
            elif snake.get_head_position() == orange.position:
                ob.position = ob_position
                flag = True
                for _ in range(snake.length // 10 * 3):
                    snake.positions.pop()
            # Удаляем gold при его поедании
            elif snake.get_head_position() == plum.position:
                ob.position = ob_position
                flag = True
                cont += 1
        snake.draw()
        score_font = font.render(f"Cчёт: {snake.score}", 1,
                                 (250, 160, 70))
        speed_font = font.render(f"Скорость: {speed}", 1, (250, 160, 70))
        level_font = font.render(f"Уровень: {level}", 1,
                                 (250, 160, 70))
        screen.blit(score_font, (655, 160))
        best_score_font = font.render(f"Рекорд: {best_score}", 1, (250, 160, 70))
        screen.blit(best_score_font, (655, 200))
        screen.blit(speed_font, (655, 240))
        screen.blit(level_font, (655, 280))
        pg.display.update()

def manual():
    screen = pg.display.set_mode((800, 600), 0, 32)
    pg.display.set_caption('Изгиб питона')
    pg.init()
    while True:
        # Копирует готовую тему.
        mytheme = pygame_menu.themes.THEME_DARK.copy()
        # Изменяет стиль шрифта для кнопок.
        mytheme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        # Изменяет стиль шрифта для заголовка.
        mytheme.title_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        # Изменяем стиль заголовка.
        mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE
        # Изменяет цвет фона в меню (последний аргумент прозрачность).
        mytheme.background_color = (215, 215, 215, 0),
        # Изменяет цвет меню.
        mytheme.widget_font_color = (0, 0, 0),
        # Изменяет цвет заголовка.
        mytheme.title_font_color = (0, 0, 0)
        # Изменяет размер заголовка.
        mytheme.title_font_size = 30
        # Создание окна и виджета меню.
        menu = pygame_menu.Menu('', 660, 600,
                                theme=mytheme)
        image_path = 'manual.png'
        menu.add.image(image_path, scale=(1, 1))
        menu.add.button('Назад', main_menu)

        while True:
            screen.fill(BOARD_BACKGROUND_COLOR)
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
            if menu.is_enabled():
                menu.draw(screen)
                menu.update(events)
            pg.display.update()
def main_menu():
    """Главное меню игры"""
    # Создает поверхность для меню.
    screen = pg.display.set_mode((250, 480), 0, 32)
    pg.display.set_caption('Изгиб питона')
    pg.init()
    while True:
        # Копирует готовую тему.
        mytheme = pygame_menu.themes.THEME_DARK.copy()
        # Изменяет стиль шрифта для кнопок.
        mytheme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        # Изменяет стиль шрифта для заголовка.
        mytheme.title_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        # Изменяем стиль заголовка.
        mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE
        # Изменяет цвет фона в меню (последний аргумент прозрачность).
        mytheme.background_color = (215,215, 215, 0),
        # Изменяет цвет меню.
        mytheme.widget_font_color = (0, 0, 0),
        # Изменяет цвет заголовка.
        mytheme.title_font_color= (0, 0, 0)
        # Изменяет размер заголовка.
        mytheme.title_font_size = 30
        # Создание окна и виджета меню.
        menu = pygame_menu.Menu('Меню',200, 200,
                                position=(25, 240, False),
                                theme=mytheme)
        menu.add.button('Играть', main)
        menu.add.button('Правила', manual)
        menu.add.button('Выход', pygame_menu.events.EXIT)
        while True:
            screen.fill(BOARD_BACKGROUND_COLOR)
            screen.blit(images['logo_menu'], (0, 0))
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
            if menu.is_enabled():
                menu.draw(screen)
                menu.update(events)
            pg.display.update()

if __name__ == '__main__':
    main_menu()