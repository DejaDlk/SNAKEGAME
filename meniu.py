import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Times New Roman', 30)
        self.buttons = ['Žaisti','Parametrai', 'Išeiti']
        self.selected_button = 0


    def draw(self):
        self.screen.fill((44, 44, 44))
        text = self.font.render('Rinkite obuolius ir saugokitės sienų! Žaidžiam?', True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(text, text_rect)

        # i - indeksas, button_text - elementas
        for i, button_text in enumerate(self.buttons):
            color = (255, 255, 255) if i == self.selected_button else (150, 150, 150)
            text_surface = self.font.render(button_text, True, color)
            text_rect = text_surface.get_rect(center=(300, 250 + i * 50))
            self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_button = (self.selected_button - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected_button = (self.selected_button + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                return self.selected_button


