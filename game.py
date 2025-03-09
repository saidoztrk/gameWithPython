import pygame
import sys
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutu
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sonsuz Kaydırmalı Oyun")

# Renkler
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
SAND = (237, 201, 175)
DARK_SAND = (210, 180, 140)
BLACK = (0, 0, 0)

# Karakter
character = pygame.Surface((50, 50))
character.fill(BLUE)
character_rect = character.get_rect()
character_rect.x, character_rect.y = 100, HEIGHT - 150

# Coinler
coin_radius = 10
coins = []

def generate_coins():
    return [pygame.Rect(random.randint(100, WIDTH * 3), random.randint(100, HEIGHT - 100), coin_radius*2, coin_radius*2) for _ in range(10)]

coins = generate_coins()

# Karakter hareket hızı
CHARACTER_SPEED = 5

# Kamera ofseti
camera_x = 0

# Yıldızlar
stars = {1: 0, 2: 0, 3: 0}  # Yıldızlar sayısal olarak temsil edilir: 0, 1, 2 veya 3

# Bölüm geçişi
current_level = 1

# Bitiş çizgisi
finish_line_x = WIDTH * 3 - 200  # Bitiş çizgisi sonu

def draw_background():
    screen.fill(SAND)
    for i in range(0, WIDTH * 3, 200):
        pygame.draw.polygon(screen, DARK_SAND, [(i - camera_x, HEIGHT - 100), (i + 200 - camera_x, HEIGHT - 80), (i + 100 - camera_x, HEIGHT - 50)])

def update_character():
    global camera_x
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_rect.x -= CHARACTER_SPEED
    if keys[pygame.K_RIGHT]:
        character_rect.x += CHARACTER_SPEED
    
    if character_rect.x > WIDTH // 2:
        camera_x = character_rect.x - WIDTH // 2

def draw_finish_line():
    pygame.draw.rect(screen, BLACK, (finish_line_x - camera_x, HEIGHT - 200, 10, 200))  # Bitiş çizgisi

def draw_stars_for_level(level, x_pos, y_pos, is_main_menu=True):
    font = pygame.font.Font(None, 30)
    for i in range(3):
        x = x_pos + i * 30
        y = y_pos
        if i < stars[level]:
            pygame.draw.polygon(screen, GOLD, [(x, y), (x + 10, y), (x + 5, y + 10)])
        elif is_main_menu:  # Ana menüde yıldızları göster
            pygame.draw.polygon(screen, BLACK, [(x, y), (x + 10, y), (x + 5, y + 10)])

def game_loop(level):
    global camera_x, coins, stars, finish_line_x, character_rect, current_level
    
    if level == 1:
        running = True
        coins = generate_coins()
        collected_coins = 0  # Toplanan coin sayısı
        while running:
            screen.fill(WHITE)
            draw_background()
            draw_finish_line()
            update_character()
            screen.blit(character, (character_rect.x - camera_x, character_rect.y))

            # Coinler çizilir
            for coin in coins[:]:
                pygame.draw.circle(screen, GOLD, (coin.x - camera_x + coin_radius, coin.y + coin_radius), coin_radius)
                if character_rect.colliderect(coin):
                    coins.remove(coin)
                    collected_coins += 1
                    
            # Yıldız kazanımı
            if collected_coins >= 8:
                stars[1] = 3
            elif collected_coins >= 5:
                stars[1] = 2
            if collected_coins == len(coins):
                stars[1] = 3

            # Bitiş çizgisine ulaşıldığında
            if character_rect.x > finish_line_x:
                running = False
                show_message("Tebrikler, bölümü geçtiniz!")
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.time.delay(30)

    elif level == 2:
        if stars[1] > 0:  # İlk bölümde en az 1 yıldız kazanıldıysa ikinci bölüme geçilebilir
            running = True
            coins = generate_coins()
            collected_coins = 0  # Toplanan coin sayısı
            while running:
                screen.fill(WHITE)
                draw_background()
                draw_finish_line()
                update_character()
                screen.blit(character, (character_rect.x - camera_x, character_rect.y))

                # Coinler çizilir
                for coin in coins[:]:
                    pygame.draw.circle(screen, GOLD, (coin.x - camera_x + coin_radius, coin.y + coin_radius), coin_radius)
                    if character_rect.colliderect(coin):
                        coins.remove(coin)
                        collected_coins += 1
                        
                # Yıldız kazanımı
                if collected_coins >= 8:
                    stars[2] = 3
                elif collected_coins >= 5:
                    stars[2] = 2
                if collected_coins == len(coins):
                    stars[2] = 3

                # Bitiş çizgisine ulaşıldığında
                if character_rect.x > finish_line_x:
                    running = False
                    show_message("Tebrikler, bölümü geçtiniz!")
                
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                pygame.time.delay(30)

    elif level == 3:
        if stars[2] > 0:  # İkinci bölümde en az 1 yıldız kazanıldıysa üçüncü bölüme geçilebilir
            running = True
            coins = generate_coins()
            collected_coins = 0  # Toplanan coin sayısı
            while running:
                screen.fill(WHITE)
                draw_background()
                draw_finish_line()
                update_character()
                screen.blit(character, (character_rect.x - camera_x, character_rect.y))

                # Coinler çizilir
                for coin in coins[:]:
                    pygame.draw.circle(screen, GOLD, (coin.x - camera_x + coin_radius, coin.y + coin_radius), coin_radius)
                    if character_rect.colliderect(coin):
                        coins.remove(coin)
                        collected_coins += 1
                        
                # Yıldız kazanımı
                if collected_coins >= 8:
                    stars[3] = 3
                elif collected_coins >= 5:
                    stars[3] = 2
                if collected_coins == len(coins):
                    stars[3] = 3

                # Bitiş çizgisine ulaşıldığında
                if character_rect.x > finish_line_x:
                    running = False
                    show_message("Tebrikler, bölümü geçtiniz!")
                
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                pygame.time.delay(30)

def show_message(message):
    font = pygame.font.Font(None, 50)  # Fontu burada kullanıyoruz
    text = font.render(message, True, BLUE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def draw_main_menu():
    font = pygame.font.Font(None, 40)  # Font burada da tanımlanmalı
    screen.fill(WHITE)
    title = font.render("Sonsuz Kaydırmalı Oyun", True, BLUE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    # Bölüm 1 (her zaman açık)
    pygame.draw.rect(screen, GOLD, (150, 130, 200, 100))
    text1 = font.render("Bölüm 1", True, BLACK)
    screen.blit(text1, (150 + 70, 130 + 10))
    draw_stars_for_level(1, 150, 200, is_main_menu=True)  # Yıldızlar sadece ana ekranda gösterilecek

    # Bölüm 2 (eğer bölüm 1'den 1 yıldız alınmışsa açık)
    if stars[1] > 0:
        pygame.draw.rect(screen, GOLD, (150, 270, 200, 100))
        text2 = font.render("Bölüm 2", True, BLACK)
        screen.blit(text2, (150 + 70, 270 + 10))
        draw_stars_for_level(2, 150, 340, is_main_menu=True)  # Yıldızlar sadece ana ekranda gösterilecek
    else:
        pygame.draw.rect(screen, (150, 150, 150), (150, 270, 200, 100))
        text2 = font.render("Bölüm 2 (Kilitli)", True, BLACK)
        screen.blit(text2, (150 + 70, 270 + 10))

    # Bölüm 3 (eğer bölüm 2'den 1 yıldız alınmışsa açık)
    if stars[2] > 0:
        pygame.draw.rect(screen, GOLD, (150, 410, 200, 100))
        text3 = font.render("Bölüm 3", True, BLACK)
        screen.blit(text3, (150 + 70, 410 + 10))
        draw_stars_for_level(3, 150, 480, is_main_menu=True)  # Yıldızlar sadece ana ekranda gösterilecek
    else:
        pygame.draw.rect(screen, (150, 150, 150), (150, 410, 200, 100))
        text3 = font.render("Bölüm 3 (Kilitli)", True, BLACK)
        screen.blit(text3, (150 + 70, 410 + 10))

    pygame.display.flip()

def main_menu():
    global current_level
    running = True
    while running:
        draw_main_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Bölüm 1'e tıklandığında
                if 150 <= mouse_x <= 350 and 130 <= mouse_y <= 230:
                    current_level = 1
                    game_loop(current_level)
                # Bölüm 2'ye tıklandığında
                elif stars[1] > 0 and 150 <= mouse_x <= 350 and 270 <= mouse_y <= 370:
                    current_level = 2
                    game_loop(current_level)
                # Bölüm 3'e tıklandığında
                elif stars[2] > 0 and 150 <= mouse_x <= 350 and 410 <= mouse_y <= 510:
                    current_level = 3
                    game_loop(current_level)

    pygame.quit()
    sys.exit()

main_menu()
