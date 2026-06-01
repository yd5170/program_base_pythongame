# 타이틀 씬 (Title Scene)

import pygame
import math
import os
from scenes.scene_base import Scene
from config import WIDTH, HEIGHT, BLACK, WHITE, NEON_GREEN, NEON_BLUE, NEON_PINK, IMG_PATH

class TitleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # 폰트 로드 (Font Load)
        self.title_font = pygame.font.SysFont("malgungothic", 80, bold=True)
        self.sub_font = pygame.font.SysFont("malgungothic", 30, bold=True)
        self.desc_font = pygame.font.SysFont("malgungothic", 22)
        
        # 배경 이미지 로드 시도 (Try to load background image)
        self.bg_image = None
        bg_path = os.path.join(IMG_PATH, "bg_title.png")
        if os.path.exists(bg_path):
            try:
                raw_bg = pygame.image.load(bg_path).convert_alpha()
                self.bg_image = pygame.transform.scale(raw_bg, (WIDTH, HEIGHT))
                # 페이드인 효과를 위한 투명도 변수 (Alpha variable for fade-in effect)
                self.bg_alpha = 0
            except Exception as e:
                print(f"배경 이미지 로딩 실패: {e}")
        
        # 심전도 (ECG) 그래프 애니메이션을 위한 변수들
        self.ecg_points = []
        self.ecg_x = 0
        self.pulse_timer = 0
        self.pulse_phase = 0  # 0: 대기, 1: P파, 2: Q파, 3: R파, 4: S파, 5: T파, 6: 회복
        self.pulse_duration = 40  # 펄스 한 번의 총 프레임 수
        
        # 텍스트 깜빡임 속도용 타이머 (Timer for text blinking speed)
        self.blink_timer = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 스페이스바 입력 시 Stage 1 시나리오 스테이지로 전환
                    from scenes.scenario_scene import ScenarioScene
                    self.game.change_scene(ScenarioScene(self.game))

    def update(self):
        # 1. 배경 이미지 페이드인 (Background image fade-in)
        if self.bg_image and self.bg_alpha < 255:
            self.bg_alpha = min(255, self.bg_alpha + 3)
            self.bg_image.set_alpha(self.bg_alpha)
            
        # 2. 텍스트 깜빡임 업데이트 (Text blink update)
        self.blink_timer += 0.05
        
        # 3. 실시간 심전도(ECG) 시뮬레이터 (Real-time ECG Simulator)
        self.pulse_timer += 1
        
        # 100프레임마다 심장박동 펄스가 뜀 (BPM 110과 조율)
        if self.pulse_timer >= 80:
            self.pulse_timer = 0
            self.pulse_phase = 1  # 펄스 시작
        
        base_y = HEIGHT // 2 + 150  # 심전도의 기본 높이 기준선 (base baseline)
        target_y = base_y
        
        # 각 페이즈별 심전도 그래프 스파이크 수치 연산 (ECG wave calculations)
        if self.pulse_phase > 0:
            frame = self.pulse_timer
            if frame < 8:  # P파 (약한 상승)
                target_y = base_y - 12 * math.sin((frame / 8) * math.pi)
            elif frame < 12:  # Q파 (약한 하강)
                target_y = base_y + 10 * math.sin(((frame - 8) / 4) * math.pi)
            elif frame < 18:  # R파 (강력한 수직 상승 스파이크)
                target_y = base_y - 120 * math.sin(((frame - 12) / 6) * math.pi)
            elif frame < 24:  # S파 (강력한 수직 하강 스파이크)
                target_y = base_y + 60 * math.sin(((frame - 18) / 6) * math.pi)
            elif frame < 32:  # T파 (중간 크기 완만한 상승)
                target_y = base_y - 25 * math.sin(((frame - 24) / 8) * math.pi)
            else:
                self.pulse_phase = 0  # 펄스 종료 후 대기 상태
                
        # 리스트에 좌표 추가
        self.ecg_points.append((WIDTH, target_y))
        
        # 기존 점들의 x좌표를 왼쪽으로 이동시킴 (Scroll ECG to the left)
        moved_points = []
        for pt in self.ecg_points:
            new_x = pt[0] - 4  # 프레임당 4픽셀씩 왼쪽으로 이동
            if new_x > 0:
                moved_points.append((new_x, pt[1]))
        self.ecg_points = moved_points

    def draw(self, screen):
        # 검은 화면으로 지운 후 렌더링
        screen.fill(BLACK)
        
        # 1. 배경 이미지 렌더링
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            # 배경 이미지가 없을 시 세련된 기하학 그라데이션 그리기
            for i in range(HEIGHT):
                # 위쪽은 짙은 감청색, 아래쪽은 완전 검정으로 변하는 그라데이션
                color_val = max(10, 30 - int(i * 30 / HEIGHT))
                pygame.draw.line(screen, (color_val, color_val // 2, color_val + 10), (0, i), (WIDTH, i))
                
        # 2. 타이틀 네온 텍스트 효과 (Neon text glow effect)
        # 글자 그림자(네온 불빛 반사 효과)
        shadow_surf = self.title_font.render("두 손으로 쫀득하게 CPR", True, NEON_PINK)
        shadow_rect = shadow_surf.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 2 - 197))
        screen.blit(shadow_surf, shadow_rect)
        
        # 실 텍스트
        title_surf = self.title_font.render("두 손으로 쫀득하게 CPR", True, WHITE)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
        screen.blit(title_surf, title_rect)
        
        # 3. 서브 타이틀 (Sub-title)
        sub_surf = self.sub_font.render("두쫀쿠 (Dujjonku CPR)", True, NEON_BLUE)
        sub_rect = sub_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 110))
        screen.blit(sub_surf, sub_rect)
        
        # 4. CPR 중요 가이드 텍스트 (Description Box)
        pygame.draw.rect(screen, (20, 20, 30), (WIDTH // 2 - 320, HEIGHT // 2 - 40, 640, 110), border_radius=15)
        pygame.draw.rect(screen, NEON_BLUE, (WIDTH // 2 - 320, HEIGHT // 2 - 40, 640, 110), width=2, border_radius=15)
        
        desc1 = self.desc_font.render("내 앞의 소중한 사람이 갑자기 쓰러진다면?", True, WHITE)
        desc2 = self.desc_font.render("올바른 대처 순서와 110 BPM의 가슴 압박 리듬을 몸으로 익히세요!", True, NEON_YELLOW)
        screen.blit(desc1, desc1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 15)))
        screen.blit(desc2, desc2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
        
        # 5. 심전도(ECG) 라인 렌더링
        if len(self.ecg_points) > 1:
            # 발광하는 네온 효과를 위해 약간 두껍고 흐릿한 녹색 라인을 먼저 그림
            pygame.draw.lines(screen, (0, 100, 0), False, self.ecg_points, 5)
            # 중심선에는 선명한 네온 그린 라인을 그림
            pygame.draw.lines(screen, NEON_GREEN, False, self.ecg_points, 2)
            
        # 6. 스페이스바 깜빡임 가이드 (Blinking spacebar guide)
        alpha = int((math.sin(self.blink_timer * 2) + 1) * 127.5) # 0 ~ 255 사이 진동
        blink_surf = self.sub_font.render("PRESS SPACEBAR TO START", True, (alpha, alpha, 255) if alpha > 50 else (50, 50, 80))
        blink_rect = blink_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 280))
        screen.blit(blink_surf, blink_rect)
