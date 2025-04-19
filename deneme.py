import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sonsuz Platform")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 50)

        self.player_color = (255, 0, 0)
        self.player_size = 50
        self.player_pos = [400, 300]
        self.speed = 5

        self.is_jumping = False
        self.jump_velocity = -15
        self.gravity = 1
        self.vertical_velocity = 0

        self.camera_x = 0  # ekran kaydırma

        # Başlangıç engelleri + zemin
        self.obstacles = [
            pygame.Rect(300, 400, 100, 20),
            pygame.Rect(700, 350, 100, 20),
            pygame.Rect(1100, 300, 120, 20),
            pygame.Rect(0, 580, 2000, 20)  # Zemin
        ]

        self.state = "menu"
        self.selected_option = 0

    def check_vertical_collisions(self):
        player_rect = pygame.Rect(self.player_pos[0] + self.camera_x, self.player_pos[1],
                                  self.player_size, self.player_size)

        on_ground = False

        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle):
                if self.vertical_velocity > 0:  # aşağı düşüyorsa
                    self.player_pos[1] = obstacle.y - self.player_size
                    self.vertical_velocity = 0
                    on_ground = True
                elif self.vertical_velocity < 0:  # yukarı çarpıyorsa
                    self.player_pos[1] = obstacle.y + obstacle.height
                    self.vertical_velocity = 0

        return on_ground

    def handle_horizontal_collision(self, dx):
        player_rect = pygame.Rect(self.player_pos[0] + self.camera_x + dx, self.player_pos[1],
                                  self.player_size, self.player_size)

        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle):
                if dx > 0:
                    self.camera_x = obstacle.left - self.player_pos[0] - self.player_size
                elif dx < 0:
                    self.camera_x = obstacle.right - self.player_pos[0]
                return

        self.camera_x += dx

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
            self.handle_horizontal_collision(-self.speed)
        if keys[pygame.K_RIGHT]:
            self.handle_horizontal_collision(self.speed)

        # ✅ Zıplama her karede kontrol edilir (gecikme yok)
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not self.is_jumping:
            self.is_jumping = True
            self.vertical_velocity = self.jump_velocity

        # Zıplama ve düşme fiziği
        self.player_pos[1] += self.vertical_velocity
        self.vertical_velocity += self.gravity

        on_ground = self.check_vertical_collisions()
        self.is_jumping = not on_ground

        if self.player_pos[1] > 600:
            print("Game Over! Aşağıya düştün.")
            self.state = "menu"

        # Ekranı temizle
        self.screen.fill((30, 30, 30))

        # Engelleri çiz (kamera offset'ine göre kaydır)
        for obstacle in self.obstacles:
            draw_rect = pygame.Rect(obstacle.x - self.camera_x, obstacle.y,
                                    obstacle.width, obstacle.height)
            pygame.draw.rect(self.screen, (0, 255, 0), draw_rect)

        # Oyuncuyu çiz (ekranda sabit)
        player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1],
                                  self.player_size, self.player_size)
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
                                self.player_pos = [400, 300]
                                self.is_jumping = False
                                self.vertical_velocity = 0
                                self.camera_x = 0
                            elif self.selected_option == 1:
                                pygame.quit()
                                sys.exit()

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "playing":
                self.run_game()

            pygame.display.update()
            self.clock.tick(60)

Game().run()
