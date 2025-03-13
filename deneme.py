import pygame
import sys
import random

pygame.init()

# Pencere ayarları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Macerası")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (10, 10, 40)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PORTAL_COLOR = (255, 0, 255)

# Zamanlama
clock = pygame.time.Clock()
FPS = 60

# Karakter özellikleri
player_radius = 20
character_rect = pygame.Rect(100, HEIGHT - 100, player_radius * 2, player_radius * 2)

# Global Değişkenler
CHARACTER_SPEED = 5
JUMP_FORCE = -15
gravity = 1
velocity_y = 0
on_ground = False
double_jump = False  # Çift zıplama özelliği

# Kamera
camera_x = 0

# Oyun durumu
lives = 3
coin_count = 0
level = 1
difficulty = "normal"  # Zorluk seviyesi
game_paused = False

# Platformlar, coinler ve düşmanlar
platforms = []
coins = []
enemies = pygame.sprite.Group()
moving_platforms = []  # Hareketli platformlar
portal_rect = pygame.Rect(0, 0, 50, 50)

# Fontlar
font = pygame.font.Font(None, 36)

# Güçlendirmeler
powerups = []

# Hikaye ve görevler
story = "Kayıp hazineyi bul ve kötü adamı yen!"
mission = f"Görev: {level * 10} coin topla ve portala ulaş!"

# Zorluk seviyeleri
def set_difficulty(diff):
    global lives, CHARACTER_SPEED, JUMP_FORCE, gravity
    if diff == "easy":
        lives = 5
        CHARACTER_SPEED = 6
        JUMP_FORCE = -16
        gravity = 0.8
    elif diff == "normal":
        lives = 3
        CHARACTER_SPEED = 5
        JUMP_FORCE = -15
        gravity = 1
    elif diff == "hard":
        lives = 1
        CHARACTER_SPEED = 4
        JUMP_FORCE = -14
        gravity = 1.2

# Platform oluşturma
def generate_platforms(level):
    plats = [pygame.Rect(0, HEIGHT - 40, WIDTH * 3, 40)]  # İlk büyük platform
    platform_height = HEIGHT - 120

    for i in range(level * 7):  # 7 platform yaratıyoruz
        width = random.randint(80, 160)
        x = random.randint(200, WIDTH * 3)
        y = platform_height - random.randint(60, 120)
        platform_height = y
        plats.append(pygame.Rect(x, y, width, 20))

        # Hareketli platformlar
        if random.choice([True, False]):
            moving_platforms.append({"rect": pygame.Rect(x, y, width, 20), "direction": 1, "speed": 2})
    return plats

# Coin oluşturma
def generate_coins(level):
    coin_list = []
    for i in range(level * 10):
        x = random.randint(200, WIDTH * 3)
        y = random.randint(100, HEIGHT - 100)
        coin_list.append(pygame.Rect(x, y, 16, 16))
    return coin_list

# Düşman sınıfı
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = random.choice([2, -2])

    def update(self):
        self.rect.x += self.velocity_x
        if self.rect.x <= 0 or self.rect.x >= WIDTH - 30:
            self.velocity_x *= -1

# Güçlendirme sınıfı
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN if type == "health" else BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Yeni seviye yükleme
def load_new_level(level):
    global platforms, coins, enemies, portal_rect, powerups
    platforms = generate_platforms(level)
    coins = generate_coins(level)
    enemies = pygame.sprite.Group()
    for _ in range(level * 2):
        enemy = Enemy(random.randint(200, WIDTH * 3), random.randint(100, HEIGHT - 100))
        enemies.add(enemy)
    
    # Portal ve güçlendirmeler
    portal_rect.x = random.randint(WIDTH // 2, WIDTH * 2)
    portal_rect.y = random.randint(100, HEIGHT - 150)
    powerups = [PowerUp(random.randint(200, WIDTH * 3), random.randint(100, HEIGHT - 100), random.choice(["health", "speed"]))]

# Arka plan çizimi
def draw_background():
    screen.fill(DARK_BLUE)
    for i in range(0, WIDTH * 3, 80):
        pygame.draw.circle(screen, WHITE, (i - camera_x % WIDTH, 50), 1)
        pygame.draw.circle(screen, WHITE, (i - camera_x % WIDTH, 100), 1)

# Oyun döngüsü
def game_loop():
    global camera_x, velocity_y, on_ground, double_jump, lives, coin_count, level, game_paused, CHARACTER_SPEED

    load_new_level(level)
    running = True
    while running:
        screen.fill(DARK_BLUE)
        draw_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_paused = not game_paused

        if game_paused:
            pause_text = font.render("Duraklatıldı (Devam etmek için P'ye basın)", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - 200, HEIGHT // 2))
            pygame.display.flip()
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            character_rect.x -= CHARACTER_SPEED
        if keys[pygame.K_d]:
            character_rect.x += CHARACTER_SPEED
        if keys[pygame.K_w]:
            if on_ground:
                velocity_y = JUMP_FORCE
                on_ground = False
            elif double_jump:
                velocity_y = JUMP_FORCE
                double_jump = False

        velocity_y += gravity
        character_rect.y += velocity_y

        # Platform çarpışma kontrolü
        on_ground = False
        for platform in platforms:
            if character_rect.colliderect(platform) and velocity_y >= 0:
                character_rect.bottom = platform.top
                velocity_y = 0
                on_ground = True

        # Hareketli platformlar
        for mp in moving_platforms:
            mp["rect"].x += mp["direction"] * mp["speed"]
            if mp["rect"].x <= 0 or mp["rect"].x >= WIDTH * 3 - mp["rect"].width:
                mp["direction"] *= -1
            if character_rect.colliderect(mp["rect"]) and velocity_y >= 0:
                character_rect.bottom = mp["rect"].top
                velocity_y = 0
                on_ground = True

        # Düşman çarpışması
        for enemy in enemies:
            if character_rect.colliderect(enemy.rect):
                lives -= 1
                enemy.rect.x = random.randint(200, WIDTH * 3)
                enemy.rect.y = random.randint(100, HEIGHT - 100)

        # Kamera hareketi
        if character_rect.x > WIDTH // 2:
            camera_x = character_rect.x - WIDTH // 2

        # Karakter çizimi
        pygame.draw.rect(screen, GREEN, (character_rect.x - camera_x, character_rect.y, character_rect.width, character_rect.height))

        # Platformlar, coinler, düşmanlar ve güçlendirmeler çizimi
        for plat in platforms:
            pygame.draw.rect(screen, (100, 100, 255), (plat.x - camera_x, plat.y, plat.width, plat.height))
        for coin in coins[:]:
            pygame.draw.circle(screen, GOLD, (coin.x - camera_x + 8, coin.y + 8), 8)
            if character_rect.colliderect(coin):
                coins.remove(coin)
                coin_count += 1
        for enemy in enemies:
            enemy.update()
            screen.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y))
        for powerup in powerups:
            screen.blit(powerup.image, (powerup.rect.x - camera_x, powerup.rect.y))
            if character_rect.colliderect(powerup.rect):
                if powerup.type == "health":
                    lives += 1
                elif powerup.type == "speed":
                    CHARACTER_SPEED += 2
                powerups.remove(powerup)

        # Portal çizimi ve çarpışma kontrolü
        pygame.draw.rect(screen, PORTAL_COLOR, (portal_rect.x - camera_x, portal_rect.y, portal_rect.width, portal_rect.height))
        if character_rect.colliderect(portal_rect) and coin_count >= level * 10:
            level += 1
            coin_count = 0
            load_new_level(level)

        # UI çizimi
        coin_text = font.render(f"Coins: {coin_count}", True, GOLD)
        life_text = font.render(f"Lives: {lives}", True, RED)
        mission_text = font.render(mission, True, WHITE)
        screen.blit(coin_text, (10, 10))
        screen.blit(life_text, (10, 40))
        screen.blit(mission_text, (10, 70))

        # Oyun sonu kontrolü
        if lives <= 0:
            game_over = font.render("Game Over", True, RED)
            screen.blit(game_over, (WIDTH // 2 - 80, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Oyun döngüsünü başlat
game_loop()
