import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sonsuz Platform")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 50)

        # Oyuncu özellikleri
        self.player_size = 100  # Karakterin boyutu 10 kat büyütüldü
        self.player_pos = [400, 400]  # Başlangıç pozisyonu
        self.speed = 5
        self.gravity = 1
        self.jump_velocity = -15
        self.vertical_velocity = 0
        self.is_jumping = False

        # Kamera kaydırma
        self.camera_x = 0

        # Animasyon resimleri
        self.animations = {
            "idle": [pygame.image.load(f"data/images/entities/player/idle/{str(i).zfill(2)}.png") for i in range(22)],  # 00.png'dan 21.png'ye kadar
            "jump": [pygame.image.load("data/images/entities/player/jump/0.png")],  # Yalnızca 0.png var
            "run": [pygame.image.load(f"data/images/entities/player/run/{i}.png") for i in range(8)],  # 0.png'dan 7.png'ye kadar
            "slide": [pygame.image.load("data/images/entities/player/slide/0.png")],  # Yalnızca 0.png var
            "wall_slide": [pygame.image.load("data/images/entities/player/wall_slide/0.png")],  # Yalnızca 0.png var
        }

        self.state = "menu"
        self.selected_option = 0
        self.current_animation = self.animations["idle"]
        self.animation_index = 0
        self.animation_speed = 0.1  # Animasyon hızını ayarla (hızlı geçiş için düşük değer)
        self.animation_time = 0

        # Arka plan resmi
        self.background = pygame.image.load("data/images/background2.png").convert()
        self.background = pygame.transform.scale(self.background, (800, 600))

        # Zemin rengi
        self.ground_level = 500  # Zemin seviyesi (karakterin duracağı yer)

    def check_vertical_collisions(self):
        player_rect = pygame.Rect(self.player_pos[0] + self.camera_x, self.player_pos[1],
                                  self.player_size, self.player_size)

        on_ground = False

        # Zemin ile çarpışmayı kontrol et
        if player_rect.colliderect(pygame.Rect(0, self.ground_level, 2000, 20)):  # Sonsuz zemin
            if self.vertical_velocity > 0:  # Aşağı düşüyorsa
                self.player_pos[1] = self.ground_level - self.player_size
                self.vertical_velocity = 0
                on_ground = True

        return on_ground

    def handle_horizontal_collision(self, dx):
        player_rect = pygame.Rect(self.player_pos[0] + self.camera_x + dx, self.player_pos[1],
                                  self.player_size, self.player_size)

        if player_rect.colliderect(pygame.Rect(0, self.ground_level, 2000, 20)):  # Sonsuz zemin
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

        # Sağ sol hareket
        if keys[pygame.K_LEFT]:
            self.handle_horizontal_collision(-self.speed)
            self.current_animation = self.animations["run"]  # Sol hareket ederken koşma animasyonu
        elif keys[pygame.K_RIGHT]:
            self.handle_horizontal_collision(self.speed)
            self.current_animation = self.animations["run"]  # Sağ hareket ederken koşma animasyonu
        else:
            if not self.is_jumping:
                self.current_animation = self.animations["idle"]  # Durduğunda idle animasyonu

        # ✅ Zıplama anlık kontrol
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not self.is_jumping:
            self.is_jumping = True
            self.vertical_velocity = self.jump_velocity
            self.current_animation = self.animations["jump"]  # Zıplarken jump animasyonu

        # Zıplama ve düşme fiziği
        self.player_pos[1] += self.vertical_velocity
        self.vertical_velocity += self.gravity

        on_ground = self.check_vertical_collisions()
        self.is_jumping = not on_ground

        if self.player_pos[1] > 600:  # Ekranın dışına çıkarsa oyun biter
            print("Game Over! Aşağıya düştün.")
            self.state = "menu"

        # Arka planı düzgün kaydırma
        self.screen.blit(self.background, (-self.camera_x % 800, 0))
        if self.camera_x % 800 != 0:
            self.screen.blit(self.background, (-self.camera_x % 800 - 800, 0))

        # Zemin rengini yeşil yap
        pygame.draw.rect(self.screen, (0, 255, 0), (0, self.ground_level, 2000, 20))

        # Animasyonu çizme (karakteri, resmin boyutunu düzgün şekilde ayarlayarak çizeceğiz)
        current_image = self.current_animation[int(self.animation_index) % len(self.current_animation)]

        # Boyutları büyük olduğu için resimleri yeniden boyutlandırmamız gerekebilir
        current_image = pygame.transform.scale(current_image, (self.player_size, self.player_size))

        player_rect = current_image.get_rect(center=(self.player_pos[0], self.player_pos[1]))

        self.screen.blit(current_image, player_rect)

        # Animasyon hızını ayarla
        self.animation_time += self.animation_speed
        if self.animation_time >= 1:
            self.animation_index += 1
            self.animation_time = 0
            if self.animation_index >= len(self.current_animation):
                self.animation_index = 0

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
                                self.player_pos = [400, 400]  # Başlangıç pozisyonu
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
