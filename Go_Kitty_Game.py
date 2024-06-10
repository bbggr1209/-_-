import pygame
import sys

# Pygame 초기화 및 화면 설정
pygame.init()
pygame.display.set_caption('Go Kitty')
MAX_WIDTH = 800
MAX_HEIGHT = 400

def main():
    # 화면 및 시계 설정
    screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    fps = pygame.time.Clock()
    font = pygame.font.Font(None, 36)  # 폰트 설정

    # 이미지 로드
    imgCat1 = pygame.image.load('./cat1.png')
    imgCat2 = pygame.image.load('./cat2.png')
    imgPlantDog = pygame.image.load('./plant_dog.png')

    # 이미지 크기 조정
    imgCat1 = pygame.transform.scale(imgCat1, (imgCat1.get_width() * 3, imgCat1.get_height() * 3))
    imgCat2 = pygame.transform.scale(imgCat2, (imgCat2.get_width() * 3, imgCat2.get_height() * 3))
    imgPlantDog = pygame.transform.scale(imgPlantDog, (imgPlantDog.get_width() * 2, imgPlantDog.get_height() * 2))

    # 고양이 및 장애물 초기 위치 설정
    cat_height = imgCat1.get_size()[1]
    cat_bottom = MAX_HEIGHT - cat_height
    cat_x = 50
    cat_y = cat_bottom
    cat_width = imgCat1.get_size()[0]
    
    plant_dog_height = imgPlantDog.get_size()[1]
    plant_dog_width = imgPlantDog.get_size()[0]
    plant_dog_x = MAX_WIDTH
    plant_dog_y = MAX_HEIGHT - plant_dog_height

    # 게임 상태 변수
    game_active = False
    game_over = False
    leg_swap = True
    is_go_up = False
    jump_speed = 10
    fall_speed = 5

    game_start_time = pygame.time.get_ticks()

    # 게임 루프
    while True:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        game_over = False  # 게임 오버 상태 초기화
                        game_active = False  # 게임을 시작 대기 상태로 변경
                        cat_y = cat_bottom  # 위치 초기화
                        plant_dog_x = MAX_WIDTH  # 장애물 위치 초기화
                    elif not game_active:
                        game_active = True  # 게임 시작
                        game_start_time = pygame.time.get_ticks()  # 게임 시작 시간 설정
                    if not is_go_up and cat_y == cat_bottom:
                        is_go_up = True  # 점프 시작

        # 게임 상태에 따른 화면 처리
        if not game_active and not game_over:  # 게임 시작 대기 화면
            screen.fill((255, 255, 255))
            title_surface = font.render('Press Space to Start', True, (0, 0, 0))
            title_x = (MAX_WIDTH - title_surface.get_width()) // 2
            title_y = (MAX_HEIGHT - title_surface.get_height()) // 2
            screen.blit(title_surface, (title_x, title_y))
        elif game_active and not game_over:  # 게임 진행 중
            current_time = pygame.time.get_ticks()
            score = (current_time - game_start_time) // 1000  # 점수 계산

            screen.fill((255, 255, 255))

            # 점프 처리
            if is_go_up:
                if cat_y > cat_bottom - 100:  # 점프 높이 조절
                    cat_y -= jump_speed
                else:
                    is_go_up = False
            elif cat_y < cat_bottom:
                cat_y += fall_speed
            else:
                cat_y = cat_bottom  # 점프 종료 및 초기 위치 복귀

            # 장애물 이동 및 그리기
            plant_dog_x -= 12.0
            if plant_dog_x <= -plant_dog_width:
                plant_dog_x = MAX_WIDTH
            screen.blit(imgPlantDog, (plant_dog_x, plant_dog_y))

            # 충돌 체크
            cat_rect = pygame.Rect(cat_x, cat_y, cat_width, cat_height)
            plant_dog_rect = pygame.Rect(plant_dog_x, plant_dog_y, plant_dog_width, plant_dog_height)
            if cat_rect.colliderect(plant_dog_rect):
                game_over = True

            # 고양이 이미지 토글 및 화면 갱신
            if not is_go_up:  # 점프 중이 아닐 때만 다리 이미지 토글
                screen.blit(imgCat1 if leg_swap else imgCat2, (cat_x, cat_y))
                leg_swap = not leg_swap
            else:
                screen.blit(imgCat1, (cat_x, cat_y))  # 점프 중에는 cat1 이미지 사용

            # 점수 표시
            score_surface = font.render(f'Score: {score}', True, (0, 0, 0))
            screen.blit(score_surface, (10, 10))
        elif game_over:  # 게임 오버 화면
            screen.fill((255, 255, 255))
            game_over_surface = font.render(f'Game Over! Score: {score} - Press Space to Restart', True, (0, 0, 0))
            go_x = (MAX_WIDTH - game_over_surface.get_width()) // 2
            go_y = (MAX_HEIGHT - game_over_surface.get_height()) // 2
            screen.blit(game_over_surface, (go_x, go_y))

        pygame.display.update()
        fps.tick(30)

if __name__ == '__main__':
    main()
    pygame.quit()
