import sys

import pygame

class Game:  # Oyun sınıfı oluşturuldu
    def __init__(self):    # Oyun sınıfının yapıcı metodu
        pygame.init()      # pygame modülünü başlatır
        pygame.display.set_caption("Deneme")  # pencerenin başlığını "Deneme" olarak ayarlar
        self.screen= pygame.display.set_mode((800, 600))   # pencerenin boyutunu 800x600 piksel olarak ayarlar
        self.clock = pygame.time.Clock()    # oyun döngüsünü kontrol etmek için bir Clock nesnesi oluşturur
    def run(self):
        while True:
            for event in pygame.event.get(): # olayları kontrol eder
                if event.type == pygame.QUIT: # pencerenin kapatılmasını kontrol eder
                    pygame.quit() # pygame modülünü kapatır
                    sys.exit() # programı sonlandırır
                        
            pygame.display.update() # pencereyi günceller
            self.clock.tick(60) # oyun döngüsünü 60 FPS (Frame Per Second) hızında çalıştırır
                


Game().run() # Oyun sınıfından bir nesne oluşturur ve oyunu çalıştırır