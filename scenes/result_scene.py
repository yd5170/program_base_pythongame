# 결과 씬 (Result Scene)

import pygame
from scenes.scene_base import Scene
from config import WIDTH, HEIGHT, BLACK, WHITE, NEON_BLUE, NEON_GREEN, NEON_RED, NEON_YELLOW, NEON_PINK, DARK_GRAY

class ResultScene(Scene):
    def __init__(self, game, success, score, max_combo=0, reason=""):
        """
        결과 씬 생성자 (Result Scene constructor)
        :param success: 게임 클리어 성공 여부 (bool)
        :param score: 플레이어의 최종 획득 점수 (int)
        :param max_combo: 플레이 중 달성한 최대 콤보 수 (int)
        :param reason: 실패 시 출력할 구체적인 원인 내용 (str)
        """
        super().__init__(game)
        self.success = success
        self.score = score
        self.max_combo = max_combo
        self.reason = reason
        
        # 폰트 로드 (Fonts Setup)
        self.large_font = pygame.font.SysFont("malgungothic", 65, bold=True)
        self.grade_font = pygame.font.SysFont("malgungothic", 100, bold=True)
        self.sub_font = pygame.font.SysFont("malgungothic", 28, bold=True)
        self.info_font = pygame.font.SysFont("malgungothic", 20)
        
        # 성적 등급 판정 (Grade evaluation)
        if not self.success:
            self.grade = "F"
            self.grade_color = NEON_RED
        else:
            if self.score >= 5000:
                self.grade = "S"
                self.grade_color = NEON_PINK
            elif self.score >= 3500:
                self.grade = "A"
                self.grade_color = NEON_YELLOW
            else:
                self.grade = "B"
                self.grade_color = NEON_BLUE
                
        # 연출용 파티클 리스트 (Particles for success celebration)
        self.particles = []
        if self.success:
            import random
            for _ in range(30):
                self.particles.append({
                    "x": random.randint(100, WIDTH - 100),
                    "y": random.randint(100, HEIGHT - 200),
                    "vx": random.uniform(-3, 3),
                    "vy": random.uniform(-4, -1),
                    "color": random.choice([NEON_GREEN, NEON_BLUE, NEON_PINK, NEON_YELLOW]),
                    "size": random.randint(3, 8),
                    "life": random.randint(40, 80)
                })

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # 'R' 키 입력 시 Stage 1 시나리오부터 게임 재시작
                    from scenes.scenario_scene import ScenarioScene
                    self.game.change_scene(ScenarioScene(self.game))
                elif event.key == pygame.K_ESCAPE:
                    # 'ESC' 키 입력 시 메인 타이틀 화면으로 복귀
                    from scenes.title_scene import TitleScene
                    self.game.change_scene(TitleScene(self.game))

    def update(self):
        # 성공 시의 폭죽 파티클 업데이트 (Update success particles)
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.05  # 미세한 중력 효과
            p["life"] -= 1
        self.particles = [p for p in self.particles if p["life"] > 0]

    def draw(self, screen):
        screen.fill(BLACK)
        
        # 1. 성공 시 배경 뿜어져 나오는 폭죽 그리기
        for p in self.particles:
            alpha = int((p["life"] / 80) * 255)
            p_surf = pygame.Surface((p["size"] * 2, p["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (p["color"][0], p["color"][1], p["color"][2], alpha), (p["size"], p["size"]), p["size"])
            screen.blit(p_surf, (int(p["x"]) - p["size"], int(p["y"]) - p["size"]))
            
        # 2. 결과 상태 메인 타이틀 렌더링 (Result banner)
        if self.success:
            title_text = "MISSION SUCCESS"
            title_color = NEON_GREEN
        else:
            title_text = "MISSION FAILED"
            title_color = NEON_RED
            
        title_surf = self.large_font.render(title_text, True, title_color)
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 250)))
        
        # 3. 등급(Grade) 대형 스탬프 렌더링 (Grade visualization)
        grade_label = self.info_font.render("응급처치 전문 평가 등급", True, WHITE)
        screen.blit(grade_label, grade_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 160)))
        
        # 등급 글씨에 네온 테두리 효과
        glow_grade = self.grade_font.render(self.grade, True, self.grade_color)
        screen.blit(glow_grade, glow_grade.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 90)))
        
        # 4. 스코어보드 박스 렌더링 (Scoreboard Panel)
        pygame.draw.rect(screen, DARK_GRAY, (WIDTH // 2 - 250, HEIGHT // 2 + 10, 500, 160), border_radius=15)
        pygame.draw.rect(screen, NEON_BLUE if self.success else NEON_RED, (WIDTH // 2 - 250, HEIGHT // 2 + 10, 500, 160), width=2, border_radius=15)
        
        # 스코어 및 콤보 텍스트
        score_surf = self.sub_font.render(f"최종 획득 점수: {self.score} 점", True, WHITE)
        screen.blit(score_surf, (WIDTH // 2 - 200, HEIGHT // 2 + 30))
        
        combo_surf = self.sub_font.render(f"최대 연속 콤보: {self.max_combo} COMBO", True, NEON_YELLOW)
        screen.blit(combo_surf, (WIDTH // 2 - 200, HEIGHT // 2 + 80))
        
        # 클리어 점수 기준 안내
        from config import PASS_SCORE
        pass_guide_surf = self.info_font.render(f"(클리어 합격 기준점수: {PASS_SCORE} 점)", True, (150, 150, 170))
        screen.blit(pass_guide_surf, (WIDTH // 2 - 200, HEIGHT // 2 + 125))
        
        # 5. 실패 시 구체적 원인 텍스트 렌더링 (Failure Reason)
        if not self.success:
            reason_box_y = HEIGHT // 2 + 190
            pygame.draw.rect(screen, (30, 15, 15), (WIDTH // 2 - 400, reason_box_y, 800, 80), border_radius=10)
            pygame.draw.rect(screen, NEON_RED, (WIDTH // 2 - 400, reason_box_y, 800, 80), width=1, border_radius=10)
            
            # 실패 원인 자동 줄바꿈 렌더링
            reason_str = f"실패 사유: {self.reason}" if self.reason else "실패 사유: 기준 미만 점수로 인한 골든타임 사수 실패"
            words = reason_str.split(' ')
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                test_surf = self.info_font.render(test_line, True, WHITE)
                if test_surf.get_width() > 740:
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line = test_line
            if current_line:
                lines.append(current_line)
                
            for idx, line in enumerate(lines[:2]):  # 최대 2줄까지만 렌더링
                line_surf = self.info_font.render(line, True, NEON_YELLOW)
                screen.blit(line_surf, line_surf.get_rect(center=(WIDTH // 2, reason_box_y + 22 + idx * 25)))
                
        # 6. 바텀 안내 메시지 (Blinking control guides)
        guide_y = HEIGHT - 60 if self.success else HEIGHT - 40
        re_surf = self.sub_font.render("다시 플레이하려면 [ R ]을 누르세요", True, NEON_GREEN)
        esc_surf = self.info_font.render("메인 타이틀 화면으로 이동하려면 [ ESC ]를 누르세요", True, WHITE)
        
        screen.blit(re_surf, re_surf.get_rect(center=(WIDTH // 2, guide_y - 30)))
        screen.blit(esc_surf, esc_surf.get_rect(center=(WIDTH // 2, guide_y + 10)))
