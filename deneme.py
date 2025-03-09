import sys

import pygame

pygame.init() # pygame modülünü başlatır

pygame.display.set_caption("Deneme") # pencerenin başlığını "Deneme" olarak ayarlar
pygame.display.set_mode((800, 600)) # 800x600 boyutunda bir pencere oluşturur

clock = pygame.time.Clock() # oyun döngüsünü kontrol etmek için bir Clock nesnesi oluşturur 

while True:
    for event in pygame.event.get(): # olayları kontrol eder
        if event.type == pygame.QUIT: # pencerenin kapatılmasını kontrol eder
            pygame.quit() # pygame modülünü kapatır
            sys.exit() # programı sonlandırır
            
    pygame.display.update() # pencereyi günceller
    clock.tick(60) # oyun döngüsünü 60 FPS (Frame Per Second) hızında çalıştırır
    
