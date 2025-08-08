import pygame
import sys
import random

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0  # x축 속도
        self.vy = 0  # y축 속도

    def update(self):
        self.vy += 1  # 중력 효과
        self.x += self.vx
        self.y += self.vy
        # 화면 밖으로 나가지 않게 제한
        if self.x < 20:
            self.x = 20
        if self.x > 780:
            self.x = 780

    def jump(self):
        self.vy = -15  # 점프 힘

    def bounce_left(self):
        self.vx = -8  # 왼쪽으로 튀기

    def bounce_right(self):
        self.vx = 8   # 오른쪽으로 튀기

    def stop(self):
        self.vx = 0

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.character = Character(400, 300)
        self.platforms = []
        self.running = True
        self.score = 0
        self.last_landed_platform = None

        # 바닥에 첫 플랫폼 생성
        self.platforms.append(pygame.Rect(300, 500, 200, 5))

        # 공 위쪽으로 여러 개의 플랫폼 미리 생성
        y = 400
        while y > 0:
            plat_x = random.randint(0, 800 - 200)
            self.platforms.append(pygame.Rect(plat_x, y, 200, 5))
            y -= random.randint(80, 120)

    def run(self):
        while self.running:
            self.update()
            self.draw()

    def update(self):
        self.handle_events()
        keys = pygame.key.get_pressed()
        if self.character:
            # 방향키를 누르고 있는 동안 vx 적용
            if keys[pygame.K_LEFT]:
                self.character.bounce_left()
            elif keys[pygame.K_RIGHT]:
                self.character.bounce_right()
            else:
                self.character.stop()
            self.character.update()
        if not self.running:
            pygame.quit()
            sys.exit()

    def draw(self):
        self.screen.fill((135, 206, 235))
        for plat in self.platforms:
            pygame.draw.rect(self.screen, (0, 0, 0), plat)
        if self.character:
            pygame.draw.circle(self.screen, (0, 0, 255), (int(self.character.x), int(self.character.y)), 20)
        # 점수 표시
        font = pygame.font.SysFont(None, 28)
        score_text = font.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (30, 30))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # 왼쪽 방향키: 점프 후 왼쪽 이동
                if event.key == pygame.K_LEFT and self.character:
                    self.character.jump()
                    self.character.bounce_left()
                    self.spawn_platform_above()
                # 오른쪽 방향키: 점프 후 오른쪽 이동
                if event.key == pygame.K_RIGHT and self.character:
                    self.character.jump()
                    self.character.bounce_right()
                    self.spawn_platform_above()
                # 스페이스바: 점프만
                if event.key == pygame.K_SPACE and self.character:
                    self.character.jump()
                    self.spawn_platform_above()
        self.check_collisions()

    def spawn_platform_above(self):
        plat_width = 200
        plat_height = 5
        min_y = max(self.character.y - random.randint(100, 150), 0)
        plat_x = random.randint(0, 800 - plat_width)
        plat = pygame.Rect(plat_x, min_y, plat_width, plat_height)
        self.platforms.append(plat)
        if len(self.platforms) > 10:  # 10개 이상일 때만 삭제
            self.platforms.pop(0)

    def spawn_platform_top(self):
        plat_width = 200
        plat_height = 5
        num_platforms = random.randint(1, 5)  # 1~5개 무작위 생성
        region_top = 0
        region_bottom = 80
        mean = (region_top + region_bottom) / 2
        stddev = (region_bottom - region_top) / 4  # 표준편차 조절(값이 작을수록 중앙에 몰림)

        for _ in range(num_platforms):
            plat_x = random.randint(0, 800 - plat_width)
            # 정규분포로 y좌표 생성, 범위 밖이면 클리핑
            plat_y = int(random.gauss(mean, stddev))
            plat_y = max(region_top, min(region_bottom, plat_y))
            self.platforms.append(pygame.Rect(plat_x, plat_y, plat_width, plat_height))
        # 너무 많아지면 오래된 것부터 삭제
        while len(self.platforms) > 15:
            self.platforms.pop(0)

    def check_collisions(self):
        if not self.character:
            return
        char_rect = pygame.Rect(
            self.character.x - 20,
            self.character.y - 20,
            40, 40
        )
        landed = False
        for plat in self.platforms:
            if char_rect.colliderect(plat) and self.character.vy > 0:
                # 착지 시 y좌표를 바 위에 고정, vy와 vx 모두 0으로(굴러떨어지지 않게)
                if self.character.y + 20 - self.character.vy <= plat.top:
                    self.character.y = plat.top - 20
                    self.character.vy = 0
                    self.character.vx = 0  # 좌우 속도도 0으로
                    # 점수 증가: 이전에 착지한 플랫폼과 다를 때만
                    if self.last_landed_platform != plat:
                        self.score += 1
                        self.last_landed_platform = plat
                    landed = True
                    break
        # 화면 내리기: 공이 일정 높이(예: 300)보다 위에 있으면
        if landed and self.character.y < 300:
            diff = 300 - self.character.y
            self.character.y = 300
            for plat in self.platforms:
                plat.y += diff
            # 위쪽에 새로운 플랫폼 생성
            self.spawn_platform_top()