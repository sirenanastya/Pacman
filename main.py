import pygame
import random
import time
from class_labyrinth import Labyrinth
from class_pacman import Pacman
from class_enemy import Enemy
from class_pacman_moves import PacmanMoves
from class_move_enemy import EnemyMoves
from class_dots_and_bonus import Dots, Bonus


WIDTH, HEIGHT = 560, 650
TILE_SIZE = 20
FREE_TILES = [1, 5]
FREE_TILES_FOR_ENEMY = [1, 2, 5]
ENEMY_EVENT = 20
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
YELLOW = (245, 208, 51)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW_FOR_DOTS = (255, 230, 2)
DARK_BLUE = (0, 0, 80)
GREY = (130, 130, 120)
BLUE_FOR_BORDERS = (0, 0, 120)
WINNING_MESSAGE = ['Congrats!', 'You won!', 'Hurray!', 'Gorgeous!', 'Cool!', 'Amazing!']
LOOSING_MESSAGE = ['You lost!', 'Maybe next time...', 'You can do better!']


# создание текстового объекта
def text_objects(text, font, color=WHITE):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# создание конпки с функционалом
def button(msg, x, y, w, h, ic, ac, action=''):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(SCREEN, ac, (x, y, w, h))
        if click[0] == 1 and action:
            if action == 'level1_1':
                main((560, 650), 'pacman_light_labyrinth.txt', 350, (15, 30))
            if action == 'level2_1':
                main((560, 650), 'pacman_light_labyrinth.txt', 250, (10, 25))
            if action == 'level3_1':
                main((560, 650), 'pacman_light_labyrinth.txt', 200, (5, 20))
            if action == 'level1_2':
                main((560, 650), 'pacman_labyrinth.txt', 350, (30, 45))
            if action == 'level2_2':
                main((560, 650), 'pacman_labyrinth.txt', 250, (20, 35))
            if action == 'level3_2':
                main((560, 650), 'pacman_labyrinth.txt', 200, (15, 30))
            elif action == 'quit':
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(SCREEN, ic, (x, y, w, h))

    small_text = pygame.font.Font(None, 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), y + (h / 2))
    SCREEN.blit(text_surf, text_rect)


def game_is_over_message(message, size=115):
    coordinates = ((0, HEIGHT / 6 + 20), (WIDTH, HEIGHT * 3 / 5))
    pygame.draw.rect(SCREEN, WHITE, coordinates)
    text = pygame.font.Font(None, size)
    text_surf, text_rect = text_objects(message, text, DARK_BLUE)
    text_rect.center = ((WIDTH / 2), (HEIGHT / 2))
    SCREEN.blit(text_surf, text_rect)
    pygame.display.update()


# создание экрана меню
def game_intro():
    pygame.display.set_caption('main menu')
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        SCREEN.fill(DARK_BLUE)

        # --- текст для экрана меню ---
        large_text = pygame.font.Font(None, 115)
        text_surf, text_rect = text_objects("PAC-MAN", large_text, YELLOW)
        text_rect.center = ((WIDTH / 2), (HEIGHT / 4))
        SCREEN.blit(text_surf, text_rect)

        button("Labyrinth 1:", WIDTH / 6, 230, 100, 50, DARK_BLUE, DARK_BLUE)
        button("Level 1", WIDTH / 6, 300, 100, 50, DARK_BLUE, BLACK, 'level1_1')
        button("Level 2", WIDTH / 6, 375, 100, 50, DARK_BLUE, BLACK, 'level2_1')
        button("Level 3", WIDTH / 6, 450, 100, 50, DARK_BLUE, BLACK, 'level3_1')

        button("Labyrinth 2:", WIDTH / 6 * 3.7, 230, 100, 50, DARK_BLUE, DARK_BLUE)
        button("Level 1", WIDTH / 6 * 3.7, 300, 100, 50, DARK_BLUE, BLACK, 'level1_2')
        button("Level 2", WIDTH / 6 * 3.7, 375, 100, 50, DARK_BLUE, BLACK, 'level2_2')
        button("Level 3", WIDTH / 6 * 3.7, 450, 100, 50, DARK_BLUE, BLACK, 'level3_2')

        button("Quit", 220, 520, 100, 50, DARK_BLUE, BLACK, 'quit')
        pygame.display.update()
        pygame.time.Clock().tick(15)


def main(size, file_name, speed, start):
    pygame.display.set_caption('pac-man')
    pygame.init()
    screen = pygame.display.set_mode(size)
    # количество оставшихся жизней на начало игры
    lives_left = 2

    # появление на экране счета игрока
    large_text = pygame.font.Font(None, 24)
    text_surf, text_rect = text_objects("Score:", large_text)
    text_rect.center = ((TILE_SIZE * 5), (TILE_SIZE / 2))
    screen.blit(text_surf, text_rect)

    # количество жизней на начало игры
    message = 'You have ' + str(lives_left + 1) + ' lives left'
    small_text = pygame.font.Font(None, 24)
    text_surf, text_rect = text_objects(message, small_text)
    text_rect.center = (WIDTH // 2, HEIGHT - (TILE_SIZE // 2))
    SCREEN.blit(text_surf, text_rect)

    # счет игрока на начало игры
    score = 0
    # лабиринт (из текствого файла в двумерный список)
    labyrinth = Labyrinth(file_name)
    # пакман
    pacman = Pacman(labyrinth)
    # обычные точки
    dots = Dots()
    # точки-бонусы
    bonus = Bonus(score)
    # приведения
    red_enemy = Enemy(1, speed)
    pink_enemy = Enemy(2, speed)
    orange_enemy = Enemy(3, speed)
    enemy_moves = EnemyMoves(red_enemy, pink_enemy, orange_enemy, screen, labyrinth, pacman)
    # PacmanMoves задает движение пакмана и приведений
    pacman_moves = PacmanMoves(screen, labyrinth, pacman, score, dots, bonus, red_enemy, pink_enemy, orange_enemy)

    clock = pygame.time.Clock()
    game_over = False
    has_won = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_intro()
            elif event.type == ENEMY_EVENT:
                if pacman_moves.flag2(start):
                    enemy_moves.move_red_enemy()
                if pacman_moves.flag(start):
                    enemy_moves.move_pink_enemy()
                enemy_moves.move_orange_enemy()

        # перемещение пакмана, если игра не закончена
        if not game_over:
            direction = pacman_moves.change_pos(screen)
            if pacman_moves.get_direction(direction) == 'make_a_circle':
                # создание изображений элементов игры
                pacman_moves.make(False)
            else:
                pacman_moves.make(pacman_moves.get_direction(direction))

        # если не осталось жизней, выводится сообщение и через 3 секунды происходит переход к экранк меню
        elif game_over and (not lives_left or has_won):
            if has_won and game_over:
                message = random.choice(WINNING_MESSAGE)
                if len(message) > 13:
                    game_is_over_message(message, HEIGHT // len(message) * 2)
                else:
                    game_is_over_message(message)
            elif game_over:
                message = random.choice(LOOSING_MESSAGE)
                if len(message) > 13:
                    game_is_over_message(message, HEIGHT // len(message) * 2)
                else:
                    game_is_over_message(message)
            time.sleep(3)
            game_intro()

        # если остались жизни, внизу печатается количество жизней и через 2 секунды игра начинается заново
        # при этом съеденные точки заново не появляются
        else:
            if game_over:
                coordinates = ((0, HEIGHT - TILE_SIZE), (WIDTH, HEIGHT))
                pygame.draw.rect(screen, BLACK, coordinates)

                lives_left -= 1
                message = 'You have ' + str(lives_left + 1) + ' lives left'
                small_text = pygame.font.Font(None, 24)
                text_surf, text_rect = text_objects(message, small_text)
                text_rect.center = (WIDTH // 2, HEIGHT - (TILE_SIZE // 2))
                SCREEN.blit(text_surf, text_rect)

                # заново задаем положение пакмана и призраков
                start = pacman.start_position(labyrinth)
                pacman.set_position(start)
                start = red_enemy.start_position(1)
                red_enemy.set_position(start)
                start = orange_enemy.start_position(2)
                orange_enemy.set_position(start)
                start = pink_enemy.start_position(3)
                pink_enemy.set_position(start)
                game_over = False

        # вывод текущего счета на экран
        pacman_moves.change_score(screen)
        # проверка на то, выиграл или проиграл ли игрок
        if pacman_moves.won():
            has_won = True
            game_over = True
        elif pacman_moves.lost(1) or pacman_moves.lost(2) or pacman_moves.lost(3):
            game_over = True
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()


if __name__ == '__main__':
    game_intro()
