import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Deneme")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 50)

        # Oyuncu özellikleri
        self.player_color = (255, 0, 0)
        self.player_pos = [400, 500]
        self.player_size = 50
        self.speed = 5

        # Zıplama değişkenleri
        self.is_jumping = False
        self.jump_velocity = -15
        self.gravity = 1
        self.vertical_velocity = 0
        self.ground_level = self.player_pos[1]

        # Engeller
        self.obstacles = [
            pygame.Rect(300, 550, 100, 20),
            pygame.Rect(500, 520, 120, 20),
            pygame.Rect(150, 480, 100, 20)
        ]

        self.state = "menu"
        self.selected_option = 0

    def draw_menu(self):
        self.screen.fill((20, 20, 20))
        options = ["BAŞLAT", "ÇIKIŞ"]

        for i, text in enumerate(options):
            color = (255, 255, 255) if i != self.selected_option else (255, 0, 0)
            rendered_text = self.font.render(text, True, color)
            rect = rendered_text.get_rect(center=(400, 250 + i * 60))
            self.screen.blit(rendered_text, rect)

    def run_game(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_pos[0] -= self.speed
        if keys[pygame.K_RIGHT]:
            self.player_pos[0] += self.speed

        # Zıplama fiziği
        if self.is_jumping:
            self.player_pos[1] += self.vertical_velocity
            self.vertical_velocity += self.gravity

            if self.player_pos[1] >= self.ground_level:
                self.player_pos[1] = self.ground_level
                self.is_jumping = False
                self.vertical_velocity = 0

        self.screen.fill((30, 30, 30))

        # Engelleri çiz
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, (0, 255, 0), obstacle)

        # Oyuncuyu çiz
        player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], self.player_size, self.player_size)
        pygame.draw.rect(self.screen, self.player_color, player_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.state == "menu":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.selected_option = (self.selected_option - 1) % 2
                        elif event.key == pygame.K_DOWN:
                            self.selected_option = (self.selected_option + 1) % 2
                        elif event.key == pygame.K_RETURN:
                            if self.selected_option == 0:
                                self.state = "playing"
                            elif self.selected_option == 1:
                                pygame.quit()
                                sys.exit()
                elif self.state == "playing":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                        elif event.key == pygame.K_SPACE:
                            if not self.is_jumping:
                                self.is_jumping = True
                                self.vertical_velocity = self.jump_velocity

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "playing":
                self.run_game()

            pygame.display.update()
            self.clock.tick(60)

Game().run()
