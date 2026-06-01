import pygame  # [엔진] 게임 제작의 핵심 도구함 (안정적인 3.11.9 버전 사용)
import sys     # [시스템] 프로그램 강제 종료 등 윈도우 제어 도구

# 1. 환경 설정 (The Stage)
pygame.init() # 게임 엔진의 전원을 켭니다.
screen = pygame.display.set_mode((1280, 720)) # 도화지 크기 설정 (DA팀의 배경 이미지 규격)
pygame.display.set_caption("두쫀쿠 - 로직 테스트 모드, 스페이스를 마구 눌러보기.") # 창 상단 제목
clock = pygame.time.Clock() # 게임의 심박수(프레임)를 일정하게 유지하는 메트로놈

# 2. 임시 객체 생성 (The Props)
# [DA팀 주목] 실제 이미지가 오기 전까지 사용하는 '가상 스프라이트'입니다.
player_idle = pygame.Surface((200, 200)) # 대기 상태의 상자 생성
player_idle.fill((0, 255, 0)) # 초록색: 평온한 상태 (나중에 chr_cpr_1.png로 교체)

player_pressed = pygame.Surface((200, 200)) # 압박 상태의 상자 생성
player_pressed.fill((255, 0, 0)) # 빨간색: 압박 중인 상태 (나중에 chr_cpr_2.png로 교체)

# 3. 데이터 및 폰트 정의 (The Data)
current_view = player_idle # [상태 제어] 현재 화면에 보여줄 '모습'을 담는 변수
score = 0 # [점수 데이터] 성공 횟수를 기록
font = pygame.font.SysFont("malgungothic", 40) # [출력] 한글 지원을 위한 맑은고딕 폰트

# 4. 메인 루프 (The Heartbeat)
# 이 반복문은 프로그램이 종료될 때까지 초당 60번씩 '생각'하고 '그림'을 그립니다.
while True:
    screen.fill((30, 30, 30)) # 매 프레임마다 배경을 어두운 회색으로 새로 칠함 (잔상 제거)
    
    # [이벤트 리스너] 사용자가 하는 모든 행동(마우스, 키보드)을 감시합니다.
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 'X' 버튼을 누르면 종료
            pygame.quit()
            sys.exit()
            
        # [AA팀 로직] 스페이스바를 누르는 시점이 바로 '가슴 압박'의 판정 시점입니다.
        if event.type == pygame.KEYDOWN: # 키를 누르는 순간
            if event.key == pygame.K_SPACE:
                current_view = player_pressed # 모습을 '압박 상태'로 변경
                score += 1 # 데이터상 점수를 1 증가
                
        if event.type == pygame.KEYUP: # 키에서 손을 떼는 순간
            if event.key == pygame.K_SPACE:
                current_view = player_idle # 모습을 다시 '대기 상태'로 환원

    # [렌더링] 위에서 계산된 '결과'를 화면에 도장을 찍듯 그려냅니다.
    # 1. 캐릭터 그리기: current_view가 초록일지 빨강일지는 위 로직이 결정함
    screen.blit(current_view, (540, 260)) # (x, y) 좌표에 현재 모습 출력
    
    # 2. 점수판 그리기: 실시간 변하는 score 변수를 글자로 변환하여 출력
    score_text = font.render(f"압박 횟수: {score}", True, (255, 255, 255))
    screen.blit(score_text, (50, 50))

    pygame.display.flip() # 그린 그림들을 모니터에 실제로 전송 (화면 갱신)
    clock.tick(60) # 초당 60번만 실행되도록 속도 조절 (CPU 과부하 방지)