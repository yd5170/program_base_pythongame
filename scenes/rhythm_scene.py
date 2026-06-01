# 리듬 게임 씬 (Rhythm Game Scene)

import pygame
import random
import math
from scenes.scene_base import Scene
from rhythm_engine import RhythmEngine
from config import (
    WIDTH, HEIGHT, BLACK, WHITE, NEON_BLUE, NEON_GREEN, NEON_RED, NEON_YELLOW, NEON_PINK, DARK_GRAY,
    BPM, TIMER_LIMIT, MAX_HP, PASS_SCORE, FEVER_COMBO, FEVER_DURATION
)

class Particle:
    """판정 성공 시 터져 나가는 파티클 효과 (Particle effects) 클래스"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-6, 6)
        self.vy = random.uniform(-8, 2)
        self.color = color
        self.life = random.randint(20, 40)  # 생존 프레임 수
        self.max_life = self.life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # 중력 (gravity) 작용
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            alpha = int((self.life / self.max_life) * 255)
            # 투명도를 살리기 위해 임시 서피스 생성
            size = max(2, int((self.life / self.max_life) * 8))
            p_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (self.color[0], self.color[1], self.color[2], alpha), (size, size), size)
            screen.blit(p_surf, (int(self.x) - size, int(self.y) - size))


class Note:
    """화면 오른쪽에서 판정선으로 흘러오는 리듬 노트 (Rhythm Note) 클래스"""
    def __init__(self, target_beat, target_time, is_item=False):
        self.target_beat = target_beat     # 목표 박자 번호
        self.target_time = target_time     # 도달해야 하는 절대 목표 시간 (초)
        self.is_item = is_item             # 목숨 회복 하트 아이템 여부
        self.is_active = True              # 판정이 가능한지 여부

    def get_x(self, elapsed_time, judgment_x, speed):
        """경과 시간에 따른 현재 노트의 X 좌표 계산 (물리 지연 보정)"""
        time_diff = self.target_time - elapsed_time
        return judgment_x + time_diff * speed


class RhythmScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # 엔진 및 점수 초기화
        self.engine = RhythmEngine()
        self.engine.start()
        
        # 게임 플레이 데이터 (Game stats)
        self.hp = MAX_HP
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        
        # 판정선 및 노트 물리 상수 (Note physics)
        self.JUDGMENT_X = 200              # 판정선 X 좌표
        self.NOTE_SPEED = 450              # 초당 노트 이동 픽셀 (pixels per second)
        
        # 노트 관리 큐/리스트 (Note List)
        self.notes = []
        self.next_note_beat = 1            # 다음에 생성할 박자 인덱스
        
        # 파티클 및 애니메이션 상태 (Animation states)
        self.particles = []
        self.press_scale = 1.0             # 가슴 압박 시 찌그러지는 연출 스케일 (scale)
        self.screen_shake = 0              # MISS 판정 시 화면 흔들림 잔여 강도
        
        # 피버 타임 관련 변수 (AED Fever Time)
        self.fever_active = False
        self.fever_start_time = 0
        self.fever_hits = 0
        
        # 판정 텍스트 연출용 변수 (Judgment visual text)
        self.judgment_text = ""
        self.judgment_color = WHITE
        self.judgment_alpha = 0
        
        # 폰트 로드
        self.ui_font = pygame.font.SysFont("malgungothic", 24, bold=True)
        self.large_font = pygame.font.SysFont("malgungothic", 50, bold=True)
        self.combo_font = pygame.font.SysFont("malgungothic", 38, bold=True)
        
        # CPR 가상 모델 가슴 영역 좌표
        self.chest_x = WIDTH // 2 + 150
        self.chest_y = HEIGHT // 2

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 1. 피버 타임 연타 로직 (Fever Mash mode)
                    if self.fever_active:
                        self.fever_hits += 1
                        self.score += 150  # 연타 한 번당 150점 보너스
                        self.combo += 1
                        self.max_combo = max(self.max_combo, self.combo)
                        self.press_scale = 0.7  # 수축 연출
                        self.judgment_text = "FEVER HIT!"
                        self.judgment_color = NEON_PINK
                        self.judgment_alpha = 255
                        
                        # 파티클 무더기 생성
                        for _ in range(5):
                            self.particles.append(Particle(self.chest_x, self.chest_y, NEON_PINK))
                        continue
                    
                    # 2. 일반 리듬 판정 로직 (Normal Rhythm judgment)
                    res, points = self.engine.get_judgment()
                    
                    # 중복 입력은 가볍게 무시
                    if res == "DUPLICATE":
                        continue
                        
                    if res:
                        # 판정 대상 노트 찾기 (판정선에 가장 가까운 활성 노트 찾아서 비활성화)
                        elapsed = self.engine.get_elapsed_time()
                        candidate_notes = [n for n in self.notes if n.is_active]
                        if candidate_notes:
                            # 절대시간 차이가 가장 적은 노트를 판정 대상으로 봄
                            target_note = min(candidate_notes, key=lambda n: abs(n.target_time - elapsed))
                            target_note.is_active = False
                            
                            # 만약 하트 아이템 노트를 성공적으로 맞췄다면 체력 회복
                            if target_note.is_item and res in ["PERFECT", "GREAT"]:
                                self.hp = min(MAX_HP, self.hp + 1)
                                # 획득 파티클 추가
                                for _ in range(10):
                                    self.particles.append(Particle(self.JUDGMENT_X, HEIGHT // 2 - 100, NEON_PINK))

                        # 판정에 따른 스탯 갱신
                        self.score += points
                        self.judgment_text = res
                        self.judgment_alpha = 255
                        
                        if res == "PERFECT":
                            self.combo += 1
                            self.judgment_color = NEON_GREEN
                            self.press_scale = 0.75
                            for _ in range(8):
                                self.particles.append(Particle(self.chest_x, self.chest_y, NEON_GREEN))
                        elif res == "GREAT":
                            self.combo += 1
                            self.judgment_color = NEON_YELLOW
                            self.press_scale = 0.8
                            for _ in range(5):
                                self.particles.append(Particle(self.chest_x, self.chest_y, NEON_YELLOW))
                        elif res == "MISS":
                            self.combo = 0
                            self.hp -= 1
                            self.judgment_color = NEON_RED
                            self.screen_shake = 10  # 화면 흔들림 강도 설정
                            
                        self.max_combo = max(self.max_combo, self.combo)
                        
                        # 피버 타임 진입 트리거 검사 (15콤보 이상 시 돌입)
                        if self.combo >= FEVER_COMBO and not self.fever_active:
                            self.fever_active = True
                            self.fever_start_time = pygame.time.get_ticks()
                            self.fever_hits = 0
                            self.judgment_text = "AED FEVER TIME!"
                            self.judgment_color = NEON_PINK
                            self.judgment_alpha = 255

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # 손을 떼면 서서히 원래 크기로 팽창
                    pass

    def update(self):
        elapsed = self.engine.get_elapsed_time()
        
        # 1. 제한 시간 완료 검사 (Time-over check)
        if elapsed >= TIMER_LIMIT:
            # 최종 점수가 합격선을 넘었는지 체크하여 결과 창으로 이동
            success = self.score >= PASS_SCORE
            from scenes.result_scene import ResultScene
            self.game.change_scene(ResultScene(self.game, success=success, score=self.score, max_combo=self.max_combo))
            return
            
        # 2. 체력 소진 즉시 게임 오버 검사 (Game-over check)
        if self.hp <= 0:
            from scenes.result_scene import ResultScene
            self.game.change_scene(ResultScene(self.game, success=False, score=self.score, max_combo=self.max_combo, reason="가슴 압박 불량으로 인한 생명력 전원 소진 (HP 0)"))
            return

        # 3. 피버 타임 시간 관리 (Fever time decay)
        if self.fever_active:
            now = pygame.time.get_ticks()
            if now - self.fever_start_time >= FEVER_DURATION:
                self.fever_active = False
                self.combo = 0  # 피버 완료 후 콤보는 0으로 리셋하여 밸런스 유지
                self.judgment_text = "AED 충격 완료!"
                self.judgment_color = NEON_BLUE
                self.judgment_alpha = 255

        # 4. 리듬 노트 자동 스폰 (Auto Spawn Notes)
        # 현재 시간 기준으로 미래 1.5초 이내에 도달할 노트들을 미리 생성해둔다.
        spawn_lookahead = 1.5
        while (self.next_note_beat * self.engine.beat_interval) < (elapsed + spawn_lookahead):
            # 피버 타임 중에는 노트를 생성하지 않음 (연타 모드에 집중)
            if not self.fever_active:
                target_time = self.next_note_beat * self.engine.beat_interval
                # 8박자마다 HP 회복 아이템 노트 스폰
                is_item = (self.next_note_beat % 8 == 0)
                self.notes.append(Note(self.next_note_beat, target_time, is_item))
            self.next_note_beat += 1
            
        # 5. 노트 좌표 업데이트 및 만료 노트 자동 MISS 처리
        active_notes = []
        for note in self.notes:
            note_x = note.get_x(elapsed, self.JUDGMENT_X, self.NOTE_SPEED)
            
            # 판정선을 지나치고 오차가 GREAT 범위를 아득히 넘어가면 MISS 처리
            if note.is_active and (elapsed - note.target_time) > self.engine.GREAT_RANGE:
                note.is_active = False
                # 피버 타임 중이 아닐 때만 미스 누적 및 체력 차감
                if not self.fever_active:
                    self.combo = 0
                    self.hp -= 1
                    self.judgment_text = "MISS"
                    self.judgment_color = NEON_RED
                    self.judgment_alpha = 255
                    self.screen_shake = 8
            
            # 화면 왼쪽 밖으로 나간 노트는 리스트에서 영구 제외
            if note_x > -50:
                active_notes.append(note)
        self.notes = active_notes
        
        # 6. 파티클 물리 업데이트 (Update particles)
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]
        
        # 7. 쫀득한 스케일 애니메이션 감쇄 (Chest scale recover)
        if self.press_scale < 1.0:
            self.press_scale += 0.05
            if self.press_scale > 1.0:
                self.press_scale = 1.0
                
        # 8. 판정 글자 투명도 페이드 아웃 (Text fade-out)
        if self.judgment_alpha > 0:
            self.judgment_alpha = max(0, self.judgment_alpha - 8)
            
        # 9. 화면 흔들림 감쇄 (Screen shake decay)
        if self.screen_shake > 0:
            self.screen_shake = max(0, self.screen_shake - 1)

    def draw(self, screen):
        # 1. 화면 흔들림 오프셋 계산 (Screen shake offset)
        offset_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        offset_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        
        # 흔들림이 반영된 가상 화면 버퍼 준비
        game_surf = pygame.Surface((WIDTH, HEIGHT))
        game_surf.fill(BLACK)
        
        # 2. 배경 디자인 그리드 (Grid design background)
        for x in range(0, WIDTH, 80):
            pygame.draw.line(game_surf, (15, 15, 25), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 80):
            pygame.draw.line(game_surf, (15, 15, 25), (0, y), (WIDTH, y))
            
        # 피버 타임 번쩍이는 배경 효과 (Fever dynamic background pulse)
        if self.fever_active:
            pulse = int((math.sin(pygame.time.get_ticks() * 0.02) + 1) * 20)
            fever_bg = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            fever_bg.fill((NEON_PINK[0], NEON_PINK[1], NEON_PINK[2], 10 + pulse))
            game_surf.blit(fever_bg, (0, 0))
            
        # 3. 판정 영역 그리기 (Judgment Line & Target Zone)
        # 세로 판정선
        pygame.draw.line(game_surf, DARK_GRAY, (self.JUDGMENT_X, 0), (self.JUDGMENT_X, HEIGHT), 4)
        
        # 판정 중심 링 (Neon ring)
        target_y = HEIGHT // 2 - 100
        pygame.draw.circle(game_surf, (20, 20, 30), (self.JUDGMENT_X, target_y), 40)
        pygame.draw.circle(game_surf, NEON_BLUE, (self.JUDGMENT_X, target_y), 40, 2)
        pygame.draw.circle(game_surf, NEON_BLUE, (self.JUDGMENT_X, target_y), 8, 0)
        
        # 4. 낙하 리듬 노트 렌더링 (Draw incoming notes)
        elapsed = self.engine.get_elapsed_time()
        for note in self.notes:
            if not note.is_active:
                continue
                
            note_x = note.get_x(elapsed, self.JUDGMENT_X, self.NOTE_SPEED)
            
            if note.is_item:
                # 하트 아이템 노트 (분홍빛 보석 하트 그리기)
                h_size = 22
                pts = [
                    (note_x, target_y + h_size),
                    (note_x - h_size, target_y - h_size // 3),
                    (note_x - h_size // 2, target_y - h_size),
                    (note_x, target_y - h_size // 3),
                    (note_x + h_size // 2, target_y - h_size),
                    (note_x + h_size, target_y - h_size // 3)
                ]
                pygame.draw.polygon(game_surf, NEON_PINK, pts)
                pygame.draw.polygon(game_surf, WHITE, pts, 2)
            else:
                # 일반 둥근 비트 노트 (네온 블루 서클)
                pygame.draw.circle(game_surf, NEON_BLUE, (int(note_x), target_y), 24)
                pygame.draw.circle(game_surf, WHITE, (int(note_x), target_y), 24, 2)
                
        # 5. CPR 가상 마네킹 가슴 압박 영역 렌더링 (Dynamic chest dummy scale)
        dummy_base_r = 110
        dummy_current_r = int(dummy_base_r * self.press_scale)
        
        # 가슴 판정 네온 글로우 원
        dummy_color = NEON_PINK if self.fever_active else NEON_BLUE
        glow_surf = pygame.Surface((dummy_current_r * 2 + 20, dummy_current_r * 2 + 20), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (dummy_color[0], dummy_color[1], dummy_color[2], 40), (dummy_current_r + 10, dummy_current_r + 10), dummy_current_r + 8)
        game_surf.blit(glow_surf, (self.chest_x - dummy_current_r - 10, self.chest_y - dummy_current_r - 10))
        
        # 내부 구조 바디 (가상 마네킹 가슴)
        pygame.draw.circle(game_surf, DARK_GRAY, (self.chest_x, self.chest_y), dummy_current_r)
        pygame.draw.circle(game_surf, dummy_color, (self.chest_x, self.chest_y), dummy_current_r, 4)
        
        # 가슴 중앙 가압점 표시 (하트 아이콘 형태 데코레이션)
        c_size = int(25 * self.press_scale)
        c_pts = [
            (self.chest_x, self.chest_y + c_size),
            (self.chest_x - c_size, self.chest_y - c_size // 3),
            (self.chest_x - c_size // 2, self.chest_y - c_size),
            (self.chest_x, self.chest_y - c_size // 3),
            (self.chest_x + c_size // 2, self.chest_y - c_size),
            (self.chest_x + c_size, self.chest_y - c_size // 3)
        ]
        pygame.draw.polygon(game_surf, NEON_RED, c_pts)
        
        # 가압 유도 가이드 글씨
        dummy_text = "압박지점" if not self.fever_active else "SPACE 연타!"
        d_surf = self.ui_font.render(dummy_text, True, WHITE)
        game_surf.blit(d_surf, d_surf.get_rect(center=(self.chest_x, self.chest_y + dummy_current_r + 40)))
        
        # 6. 파티클 효과 렌더링
        for p in self.particles:
            p.draw(game_surf)
            
        # 7. UI 정보 영역 렌더링 (Top HUD)
        # 상단 HUD 바
        pygame.draw.rect(game_surf, (20, 20, 30), (0, 0, WIDTH, 80))
        pygame.draw.line(game_surf, NEON_BLUE, (0, 80), (WIDTH, 80), 2)
        
        # 점수 표시
        score_surf = self.ui_font.render(f"SCORE: {self.score}", True, WHITE)
        game_surf.blit(score_surf, (40, 25))
        
        # 합격 컷오프 표시
        cut_surf = self.ui_font.render(f"(합격: {PASS_SCORE}점)", True, NEON_YELLOW)
        game_surf.blit(cut_surf, (220, 25))
        
        # 남은 시간 타이머 표시
        time_left = max(0.0, TIMER_LIMIT - elapsed)
        timer_color = NEON_RED if time_left <= 5.0 else WHITE
        timer_surf = self.ui_font.render(f"TIME: {time_left:.1f}s", True, timer_color)
        game_surf.blit(timer_surf, (WIDTH // 2 - 80, 25))
        
        # 체력 하트 표시 (HP HUD)
        for h_idx in range(MAX_HP):
            h_x = WIDTH - 180 + h_idx * 30
            h_y = 25
            hp_color = NEON_PINK if h_idx < self.hp else DARK_GRAY
            hp_pts = [
                (h_x + 10, h_y + 20),
                (h_x, h_y + 8),
                (h_x + 5, h_y + 3),
                (h_x + 10, h_y + 8),
                (h_x + 15, h_y + 3),
                (h_x + 20, h_y + 8)
            ]
            pygame.draw.polygon(game_surf, hp_color, hp_pts)
            pygame.draw.polygon(game_surf, WHITE, hp_pts, 1)

        # 8. 콤보 및 판정 텍스트 렌더링 (Combo & Judgment Display)
        # 콤보 표시
        if self.combo > 0:
            combo_title = self.ui_font.render("COMBO", True, NEON_BLUE)
            combo_val = self.combo_font.render(str(self.combo), True, WHITE)
            game_surf.blit(combo_title, combo_title.get_rect(center=(self.chest_x, self.chest_y - 200)))
            game_surf.blit(combo_val, combo_val.get_rect(center=(self.chest_x, self.chest_y - 160)))
            
        # 판정 글씨 (Fade out)
        if self.judgment_text and self.judgment_alpha > 0:
            judg_surf = self.large_font.render(self.judgment_text, True, self.judgment_color)
            # 글씨 페이드 아웃 효과를 위한 서피스 변환
            text_s = pygame.Surface(judg_surf.get_size(), pygame.SRCALPHA)
            text_s.blit(judg_surf, (0, 0))
            text_s.set_alpha(self.judgment_alpha)
            game_surf.blit(text_s, text_s.get_rect(center=(self.chest_x, self.chest_y - 250)))

        # 9. 피버 타임 연출 배너 (Fever Time Warning Banner)
        if self.fever_active:
            banner_y = HEIGHT - 180
            pygame.draw.rect(game_surf, (255, 0, 127, 200), (0, banner_y, WIDTH, 90))
            pygame.draw.line(game_surf, WHITE, (0, banner_y), (WIDTH, banner_y), 2)
            pygame.draw.line(game_surf, WHITE, (0, banner_y + 90), (WIDTH, banner_y + 90), 2)
            
            # 삐뽀거리는 비전 연출 느낌의 문구
            f_blink = int((math.sin(pygame.time.get_ticks() * 0.03) + 1) * 127.5)
            warn_color = (255, f_blink, f_blink)
            warn_surf = self.large_font.render("⚡ AED 충격 준비 완료! SPACEBAR 연타! ⚡", True, warn_color)
            game_surf.blit(warn_surf, warn_surf.get_rect(center=(WIDTH // 2, banner_y + 45)))

        # 화면에 최종 흔들림 오프셋을 적용해 대입
        screen.blit(game_surf, (offset_x, offset_y))
