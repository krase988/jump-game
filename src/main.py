import pygame
import sys
import math
from game import Game

BUTTON_RECT = pygame.Rect(680, 20, 100, 40)  # 우측 상단 버튼 위치와 크기

def draw_new_game_button(screen):
    pygame.draw.rect(screen, (255, 255, 255), BUTTON_RECT, border_radius=8)  # 흰색 버튼
    font = pygame.font.SysFont(None, 28)
    text = font.render("New Game", True, (0, 0, 0))
    text_rect = text.get_rect(center=BUTTON_RECT.center)
    screen.blit(text, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Jump Game")
    
    game = Game(screen)
    running = True

    left_pressed = False
    right_pressed = False
    press_time = 0
    direction = None  # 'left' or 'right'
    angle = 0

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTON_RECT.collidepoint(event.pos):
                    game = Game(screen)  # New Game 버튼 클릭 시 게임 재시작
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_n:
                    game = Game(screen)  # N 키로도 게임 재시작
                elif event.key == pygame.K_LEFT and game.character:
                    left_pressed = True
                    press_time = pygame.time.get_ticks()
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and game.character:
                    right_pressed = True
                    press_time = pygame.time.get_ticks()
                    direction = 'right'
                elif event.key == pygame.K_UP and game.character:
                    game.character.jump()
                elif event.key == pygame.K_SPACE and game.character:
                    game.character.jump()
                    game.spawn_platform_top()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and left_pressed:
                    if pygame.time.get_ticks() - press_time >= 1000:
                        # 1초 이상: 각도 점프
                        rad = math.radians(angle)
                        power = 15
                        vx = -power * math.cos(rad)
                        vy = -power * math.sin(rad)
                        game.character.vx = vx
                        game.character.vy = vy
                    else:
                        # 1초 미만: 기본 점프
                        game.character.jump()
                        game.character.bounce_left()
                    left_pressed = False
                    direction = None
                if event.key == pygame.K_RIGHT and right_pressed:
                    if pygame.time.get_ticks() - press_time >= 1000:
                        rad = math.radians(angle)
                        power = 15
                        vx = power * math.cos(rad)
                        vy = -power * math.sin(rad)
                        game.character.vx = vx
                        game.character.vy = vy
                    else:
                        game.character.jump()
                        game.character.bounce_right()
                    right_pressed = False
                    direction = None

        # 방향키가 눌려있지 않을 때만 update 호출
        if (left_pressed or right_pressed) and pygame.time.get_ticks() - press_time >= 1000:
            game.character.vx = 0
            game.character.vy = 0
        else:
            game.update()
        # draw는 항상 호출
        game.draw()
        draw_new_game_button(screen)

        # 빨간 선 그리기 (1초 이상 누르고 있을 때만)
        if (left_pressed or right_pressed) and pygame.time.get_ticks() - press_time >= 1000:
            t = (pygame.time.get_ticks() - press_time - 1000) / 1000  # 1초 이후부터
            angle = 45 + 45 * math.sin(t * math.pi)  # 0~90도
            if direction == 'left':
                draw_angle = 180 - angle
            else:
                draw_angle = angle
            rad = math.radians(draw_angle)
            cx, cy = int(game.character.x), int(game.character.y)
            length = 60
            ex = int(cx + length * math.cos(rad))
            ey = int(cy - length * math.sin(rad))
            pygame.draw.line(screen, (255, 0, 0), (cx, cy), (ex, ey), 4)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()