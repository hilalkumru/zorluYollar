import pygame
import random

# Ekran boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Renk tanımları
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # Kırmızı karakter ekranın alt kısmında konumlanıyor.
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)
        # Karakter ekran dışına çıkmasın diye.
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.reset_position()
        # Bu bayrak, engelin oyuncuyu geçtiğinde puan kazandırıp kazandırmadığını takip eder.
        self.passed = False

    def update(self):
        self.rect.move_ip(0, 5)
        # Engel ekranın altına tamamen çıktığında konumu resetle
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        # Yukarıdan gelmesi için negatif yükseklik veriyoruz
        self.rect.y = -self.rect.height
        self.passed = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zorlu Yollar")
    clock = pygame.time.Clock()

    # Oyuncu ve engel nesnelerini oluşturuyoruz.
    player = Player()
    obstacles = pygame.sprite.Group()
    for _ in range(10):
        obstacles.add(Obstacle())

    score = 0
    font = pygame.font.SysFont(None, 55)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update()

        # Her engeli güncelle ve oyuncuyu geçtiyse (yani engelin üst kısmı oyuncunun altını geçtiyse) puanı artır.
        last_scored_y = SCREEN_HEIGHT  # En son puan alınan engelin Y konumunu sakla

        for obstacle in obstacles:
            obstacle.update()
            if not obstacle.passed and obstacle.rect.top > player.rect.bottom:
                if obstacle.rect.top < last_scored_y:  # Sadece en alttaki engel puan kazandırsın
                    score += 1
                    last_scored_y = obstacle.rect.top
                obstacle.passed = True

        # Çarpışma kontrolü: Eğer oyuncu ile herhangi bir engel çarpışırsa oyun sonlanır.
        if pygame.sprite.spritecollideany(player, obstacles):
            running = False

        screen.fill(WHITE)
        obstacles.draw(screen)
        screen.blit(player.image, player.rect)

        # Gerçek zamanlı skoru ekrana yazdır.
        score_text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_text, (1, 1))

        pygame.display.flip()
        clock.tick(30)

    # Oyun biter bitmez final skoru gösterelim.
    screen.fill(WHITE)
    final_score_text = font.render("Final Score: " + str(score), True, BLACK)
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()
