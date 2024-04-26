import time
import pygame
from pygame.locals import *
import random
from meniu import Menu

default = 40
background = (44, 44, 44)
screen_size = (600, 600)
screen_center = (screen_size[0] // 2, screen_size[1] // 2)



class Apple:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('recourses/apple.png').convert_alpha()
        self.x = default * 1
        self.y = default * 2.5

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(1, 14) * default
        self.y = random.randint(1, 14) * default


class Orange:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('recourses/orange.png').convert_alpha()
        self.x = default * 3
        self.y = default * 3

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(1, 14) * default
        self.y = random.randint(1, 14) * default


class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.snake_images = [
            pygame.image.load("recourses/blue.jpg").convert_alpha(),
            pygame.image.load("recourses/green.jpg").convert_alpha(),
            pygame.image.load("recourses/pink.jpg").convert_alpha(),
            pygame.image.load("recourses/yellow.jpg").convert_alpha()
        ]
        self.snake_color_index = 0
        self.direction = 'down'
        self.length = 1
        self.x = [40]
        self.y = [40]

    def move(self, direction):
        self.direction = direction

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == 'left':
            self.x[0] -= default
        if self.direction == 'right':
            self.x[0] += default
        if self.direction == 'up':
            self.y[0] -= default
        if self.direction == 'down':
            self.y[0] += default
        self.draw()

    def draw(self):
        self.screen.fill(background)
        for i in range(self.length):
            self.screen.blit(self.snake_images[self.snake_color_index], (self.x[i], self.y[i]))

    def increase_length(self):
        self.length += 1
        self.x.append(1)
        self.y.append(1)

    def decrease_length(self):
        self.length -= 1
        self.x.pop()
        self.y.pop()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('Gyvatelės žaidimas')
        self.music_playing = False

        self.loading_progress = 0
        self.loading_bar_width = 400
        self.loading_bar_height = 30
        self.font = pygame.font.SysFont('Times New Roman', 50)

        self.menu = Menu(self.surface)
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.orange_obstacle = Orange(self.surface)
        self.level = 0
        self.speed = 0.5
        self.obstacle_move_time = time.time()
        self.obstacle_move_interval = 5
        self.obstacle_count = 0
        self.game_over = 0

    def show_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.menu.draw()
            pygame.display.update()

            selected_option = self.menu.handle_event(pygame.event.wait())
            if selected_option == 0:
                self.run()
            elif selected_option == 1:
                self.show_parameters_menu()
            elif selected_option == 2:
                pygame.quit()
                quit()

    def show_parameters_menu(self):
        self.snake.speed = 0
        parameters_menu = Menu(self.surface)
        parameters_menu.buttons = ['Gyvatės Spalva', 'Muzika', 'Atgal']
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            parameters_menu.draw()
            pygame.display.update()

            selected_param = parameters_menu.handle_event(pygame.event.wait())
            if selected_param == 0:
                self.choose_snake_color()
            elif selected_param == 1:
                self.sound_options()
            elif selected_param == 2:
                return

    def choose_snake_color(self):
        selected_color_index = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        selected_color_index = (selected_color_index + 1 if event.key == pygame.K_DOWN else
                                                selected_color_index - 1) % len(self.snake.snake_images)
                    elif event.key == pygame.K_RETURN:
                        self.snake.snake_color_index = selected_color_index
                        return

            self.surface.fill(background)

            text_font = pygame.font.SysFont('Times New Roman', 30)
            text = text_font.render('Pasirinkite gyvatės spalvą:', True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_center[0], 100))
            self.surface.blit(text, text_rect)

            for i, color_image in enumerate(self.snake.snake_images):
                image_rect = color_image.get_rect(center=(screen_center[0], 200 + i * 100))
                self.surface.blit(color_image, image_rect)
                if i == selected_color_index:
                    pygame.draw.rect(self.surface, (255, 255, 255), image_rect, 3)

            pygame.display.update()

    def sound_options(self):
        sound_menu = Menu(self.surface)
        sound_menu.buttons = ['Įjungti', 'Išjungti']
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            selected_option = sound_menu.handle_event(pygame.event.wait())
            if selected_option == 0:
                pygame.mixer.music.unpause()
                pygame.mixer.init()
                self.play_background_music()
                return
            elif selected_option == 1:
                pygame.mixer.music.stop()
                return

            sound_menu.draw()
            pygame.display.update()

    def draw_loading_screen(self):
        self.surface.fill(background)
        pygame.draw.rect(self.surface, (255, 255, 255), (100, 350, self.loading_bar_width, self.loading_bar_height))
        pygame.draw.rect(self.surface, (192, 192, 192),
                         (100, 350, int(self.loading_bar_width * self.loading_progress), self.loading_bar_height))
        text = self.font.render('Kraunasi....', True, (255, 255, 255))
        text_rect = text.get_rect(center=screen_center)
        self.surface.blit(text, text_rect)
        pygame.display.flip()

    def loading_process(self):
        while self.loading_progress < 1:
            time.sleep(0.2)
            self.loading_progress += 0.1
            self.draw_loading_screen()

    def reset(self):
        self.level = 1
        self.speed = 0.5
        self.obstacle_count = 0
        self.snake.length = 0
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.orange_obstacle = Orange(self.surface)

    def update_speed(self):
        self.speed += 1

    def is_collision(self, x1, y1, x2, y2):
        return x2 <= x1 < x2 + default and y2 <= y1 < y2 + default

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.orange_obstacle.draw()
        self.display_score()
        self.display_level()
        pygame.display.flip()

        # judinam apelsina
        current_time = time.time()
        if current_time - self.obstacle_move_time >= self.obstacle_move_interval:
            self.orange_obstacle.move()
            self.obstacle_move_time = current_time

        # jeigu gyvate suvalgo obuoli:
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            ding = pygame.mixer.Sound("recourses/ding.mp3")
            pygame.mixer.Sound.play(ding)
            self.snake.increase_length()
            self.apple.move()
            if self.snake.length % 3 == 0:
                self.level += 1
                self.update_speed()

        # jeigu gyvate suvalgo apelsina:
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.orange_obstacle.x, self.orange_obstacle.y):
            ding = pygame.mixer.Sound("recourses/crash.mp3")
            pygame.mixer.Sound.play(ding)
            self.snake.decrease_length()
            self.orange_obstacle.move()
            self.obstacle_count += 1

        # jeigu gyvate susidure su savimi:
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                crash = pygame.mixer.Sound("recourses/boom.mp3")
                pygame.mixer.Sound.play(crash)
                self.game_over = 0
                raise Exception('Susidūrėte su savimi!')

        # jeigu gyvate atsitrenke i siena:
        if not (0 <= self.snake.x[0] <= screen_size[0] and 0 <= self.snake.y[0] <= screen_size[1]):
            crash = pygame.mixer.Sound("recourses/boom.mp3")
            pygame.mixer.Sound.play(crash)
            self.game_over = 1
            raise Exception("Atsitrenkėte į sieną!")

    def display_level(self):
        font = pygame.font.SysFont('Times New Roman', 30)
        level_text = font.render(f'Lygis: {self.level}', True, (200, 200, 200))
        self.surface.blit(level_text, (430, 50))

    def display_score(self):
        font = pygame.font.SysFont('Times New Roman', 30)
        score = font.render(f'Taškai: {self.snake.length - 1}', True, (200, 200, 200))
        self.surface.blit(score, (430, 10))

    def show_game_over(self):
        self.surface.fill(background)

        if self.game_over == 0:
            tekstas = 'Susidūrėte su savimi!'
        else:
            tekstas = 'Atsitrenkėte į sieną!'

        font = pygame.font.SysFont('Times New Roman', 30)
        line1 = font.render(f'PRALAIMĖJOTE! {tekstas}', True, (255, 255, 255))
        self.surface.blit(line1, (50, 200))

        line3 = font.render(f'Jūsų taškai: {self.snake.length - 1}, Lygis: {self.level}', True, (255, 255, 255))
        self.surface.blit(line3, (50, 250))

        apple_image = pygame.image.load('recourses/apple.png')
        self.surface.blit(apple_image, (50, 300))
        apple_count_text = font.render(f'Jūs suvalgėte {self.snake.length - 1} obuolius', True, (255, 255, 255))
        self.surface.blit(apple_count_text, (100, 300))

        orange_image = pygame.image.load('recourses/orange.png')
        self.surface.blit(orange_image, (50, 350))
        orange_count_text = font.render(f'Jūs pagavote {self.obstacle_count} kliūtis', True, (255, 255, 255))
        self.surface.blit(orange_count_text, (100, 350))

        line2 = font.render(f'Norint žaisti dar kartą, paspauskite ENTER', True, (255, 255, 255))
        self.surface.blit(line2, (50, 400))
        pygame.display.flip()

    def play_background_music(self):
        pygame.mixer.music.load("recourses/music.mp3")
        pygame.mixer.music.play()

    def run(self):
        running = True
        pause = False
        self.draw_loading_screen()
        self.loading_process()

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move('left')
                        if event.key == K_RIGHT:
                            self.snake.move('right')
                        if event.key == K_UP:
                            self.snake.move('up')
                        if event.key == K_DOWN:
                            self.snake.move('down')

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                print(e)
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.25)


if __name__ == '__main__':
    game = Game()
    game.show_menu()
