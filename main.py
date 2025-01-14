
import pygame
import random
import math

# 初始化 Pygame
pygame.init()
pygame.mixer.init()  # 初始化混音器

# 设置全屏模式
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
pygame.display.set_caption("烟花效果模拟器")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 加载声音效果
try:
    explosion_sound = pygame.mixer.Sound("explosion.wav")
except:
    print("声音文件 'explosion.wav' 未找到，声音效果将被禁用。")
    explosion_sound = None

# 设置帧率
clock = pygame.time.Clock()
FPS = 60


# 烟花粒子类
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed, color, size=4, life=40):
        super().__init__()
        self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size, size), size)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = [random.randint(128, 255) for _ in range(3)]
        self.gravity = 0.05
        self.wind = random.uniform(-0.2, 0.2)  # 风力
        self.life = life
        self.start_life = life
        self.size = size

    def update(self):
        self.vy += self.gravity
        self.vx += self.wind
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.life -= 1
        # 逐渐变暗
        alpha = max(0, int(255 * (self.life / self.start_life)))
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image, (*self.color, alpha), (self.size, self.size), self.size
        )
        if self.life <= 0:
            self.kill()


# 烟花类
class Firework:
    def __init__(self, x=None, y=None, shape="circle"):
        self.shape = shape
        if x is None:
            self.x = random.randint(100, WIDTH - 100)
        else:
            self.x = x
        if y is None:
            self.y = HEIGHT
        else:
            self.y = y
        self.particles = pygame.sprite.Group()
        self.exploded = False
        self.speed = random.uniform(4, 7)
        self.angle = -math.pi / 2 + random.uniform(-0.1, 0.1)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.color = [random.randint(128, 255) for _ in range(3)]

    def update(self):
        if not self.exploded:
            self.x += self.vx
            self.y += self.vy
            self.vy += 0.05  # 重力
            if self.vy >= 0:
                self.explode()
        else:
            self.particles.update()

    def explode(self):
        self.exploded = True
        num_particles = random.randint(50, 100)
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            size = random.randint(2, 4)
            life = random.randint(20, 40)
            p = Particle(self.x, self.y, angle, speed, self.color, size, life)
            self.particles.add(p)
        if explosion_sound:
            explosion_sound.play()

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)
        else:
            self.particles.draw(surface)

    def is_dead(self):
        return self.exploded and len(self.particles) == 0


# 主循环
def main():
    # 空数组用于存放新变量
    fireworks = []
    # 记录总事件数
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, 1000)  # 每秒生成一个烟花

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == spawn_event:
                fireworks.append(Firework())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                fireworks.append(Firework(x=pos[0], y=pos[1], shape="circle"))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # 生成心形烟花
                    fireworks.append(Firework(x=WIDTH // 2, y=HEIGHT, shape="heart"))
                if event.key == pygame.K_2:
                    # 生成星形烟花
                    fireworks.append(Firework(x=WIDTH // 2, y=HEIGHT, shape="star"))

        # 更新烟花
        for firework in fireworks:
            firework.update()
        fireworks = [f for f in fireworks if not f.is_dead()]

        # 绘制
        screen.fill(BLACK)
        for firework in fireworks:
            firework.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
