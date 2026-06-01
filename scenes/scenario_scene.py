# 시나리오 씬 (Scenario Scene)

import pygame
from scenes.scene_base import Scene
from config import WIDTH, HEIGHT, BLACK, WHITE, NEON_BLUE, NEON_GREEN, NEON_RED, NEON_YELLOW, DARK_GRAY

class ScenarioScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # 폰트 설정 (Fonts Setup)
        self.title_font = pygame.font.SysFont("malgungothic", 45, bold=True)
        self.question_font = pygame.font.SysFont("malgungothic", 24, bold=True)
        self.option_font = pygame.font.SysFont("malgungothic", 20)
        self.info_font = pygame.font.SysFont("malgungothic", 18)
        self.feedback_font = pygame.font.SysFont("malgungothic", 28, bold=True)
        
        # 시나리오 단계 및 퀴즈 데이터 정의 (Quiz Data Structure)
        self.step = 1  # 1단계부터 시작
        self.max_steps = 3
        
        # 퀴즈 정보 딕셔너리 (Quiz details dictionary)
        self.quizzes = {
            1: {
                "situation": "상황: 길가에 한 사람이 갑자기 의식을 잃고 쓰러진 모습을 목격했습니다.",
                "question": "Q1. 환자에게 가장 먼저 취해야 할 대처 행동은 무엇입니까?",
                "options": [
                    "1. 환자의 뺨을 강하게 때리며 정신을 차리도록 소리친다.",
                    "2. 환자의 양어깨를 가볍게 두드리며 큰 목소리로 의식을 확인한다.",
                    "3. 의식 확인 없이 즉시 갈비뼈 중앙에 심폐소생술(CPR)을 가슴 압박한다."
                ],
                "answer": 2,
                "fail_reason": "의식을 잃은 환자의 얼굴을 때리는 것은 뇌 손상이나 척추 부상을 유발할 수 있으며, 의식 확인 없이 즉각적인 가슴 압박을 실시하면 미세하게 의식이 있던 환자에게 큰 부상을 입힐 수 있습니다."
            },
            2: {
                "situation": "상황: 환자의 의식이 없음을 확인하고 주변의 도움을 청해야 합니다.",
                "question": "Q2. 119 신고와 자동심장충격기(AED)를 효율적으로 요청하는 방법은?",
                "options": [
                    "1. 주변 군중을 향해 막연하게 '누가 좀 119에 신고해 주시고 AED도 가져다주세요!'라고 크게 외친다.",
                    "2. 빨간 옷이나 안경 쓴 사람 등 특정인을 명확히 지목하여 '119 신고와 AED 확보'를 정중히 요청한다.",
                    "3. 도움을 구하지 않고, 골든타임을 놓치기 전에 즉시 인공호흡을 단독으로 진행한다."
                ],
                "answer": 2,
                "fail_reason": "막연하게 외치면 구경꾼 효과(Bystander effect)로 인해 서로 눈치만 보느라 조치가 늦어집니다. 반드시 인상착의를 특정하여 지목(ex: '거기 파란 모자 쓰신 분, 119에 신고해 주세요!')해야 신속한 구조가 가능합니다."
            },
            3: {
                "situation": "상황: 구조 요청을 마친 상태에서 환자가 정상적으로 호흡을 하고 있는지 체크해야 합니다.",
                "question": "Q3. 환자의 호흡 상태를 정밀하게 파악하기 위한 정석적인 방법은?",
                "options": [
                    "1. 환자의 얼굴(코와 입)에 귀를 대고 10초간 숨소리를 듣고 가슴의 상하 요동을 관찰한다.",
                    "2. 맥박 측정을 위해 목 옆동맥(경동맥)을 손끝으로 5분 이상 깊게 눌러 본다.",
                    "3. 환자의 몸을 거꾸로 세워 흔든 뒤, 등을 두드려 기도가 혹시 막혔는지 테스트한다."
                ],
                "answer": 1,
                "fail_reason": "일반인은 위급한 상황에서 환자의 맥박을 정확히 측정하기 어렵습니다. 따라서 세계 보건 기구 지침에 따라 10초간 환자의 코와 입에 귀를 대어 호흡음을 들으며 가슴의 움직임(상하 요동)을 육안으로 확인하는 것이 원칙입니다."
            }
        }
        
        # 연출용 상태 변수 (Effect variables)
        self.feedback_text = ""
        self.feedback_color = NEON_GREEN
        self.feedback_timer = 0  # 정답/오답 연출이 화면에 잠시 멈추는 타이머 (ticks)
        self.is_failed = False
        self.is_success = False

    def handle_events(self, events):
        # 피드백이 연출 중일 때는 키 입력을 받지 않음
        if self.feedback_timer > 0:
            return
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                # 숫자 키 1, 2, 3 입력 감지 (Key detection)
                choice = 0
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    choice = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    choice = 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    choice = 3
                
                if choice > 0:
                    self.check_answer(choice)

    def check_answer(self, choice):
        current_quiz = self.quizzes[self.step]
        if choice == current_quiz["answer"]:
            # 정답인 경우 (Correct Answer)
            self.feedback_text = "정답입니다! 올바른 응급 대처 행동입니다."
            self.feedback_color = NEON_GREEN
            self.feedback_timer = 60  # 60프레임 (약 1초) 동안 대기
            self.is_success = True
        else:
            # 오답인 경우 (Wrong Answer)
            self.feedback_text = "틀렸습니다!"
            self.feedback_color = NEON_RED
            self.feedback_timer = 120  # 오답 피드백은 이유를 보여주기 위해 약 2초(120프레임) 대기
            self.is_failed = True
            self.fail_reason = current_quiz["fail_reason"]

    def update(self):
        # 피드백 타이머 제어 (Feedback timer control)
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            if self.feedback_timer == 0:
                if self.is_success:
                    self.is_success = False
                    self.feedback_text = ""
                    if self.step < self.max_steps:
                        self.step += 1
                    else:
                        # 3단계 모두 정답을 맞히면 Stage 2 리듬 게임 씬으로 진입
                        from scenes.rhythm_scene import RhythmScene
                        self.game.change_scene(RhythmScene(self.game))
                elif self.is_failed:
                    # 실패 시 결과 화면으로 즉시 전환
                    from scenes.result_scene import ResultScene
                    self.game.change_scene(ResultScene(self.game, success=False, score=0, reason=self.fail_reason))

    def draw(self, screen):
        screen.fill(BLACK)
        
        # 1. 헤더 영역 (Header Area)
        pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, 100))
        pygame.draw.line(screen, NEON_BLUE, (0, 100), (WIDTH, 100), 2)
        
        header_surf = self.title_font.render("STAGE 1: 응급 대처 시나리오", True, WHITE)
        header_rect = header_surf.get_rect(center=(WIDTH // 2, 50))
        screen.blit(header_surf, header_rect)
        
        # 2. 진행 상태 인디케이터 (Step Indicator)
        for i in range(1, self.max_steps + 1):
            circle_x = WIDTH - 180 + i * 35
            circle_y = 50
            if i < self.step:
                # 이미 통과한 단계: 녹색
                pygame.draw.circle(screen, NEON_GREEN, (circle_x, circle_y), 10)
            elif i == self.step:
                # 현재 단계: 파란색
                pygame.draw.circle(screen, NEON_BLUE, (circle_x, circle_y), 10)
            else:
                # 아직 도달하지 않은 단계: 어두운 회색
                pygame.draw.circle(screen, DARK_GRAY, (circle_x, circle_y), 10)
                pygame.draw.circle(screen, WHITE, (circle_x, circle_y), 10, 1)
        
        # 3. 상황 설명 박스 (Situation Box)
        current_quiz = self.quizzes[self.step]
        pygame.draw.rect(screen, (25, 25, 35), (50, 140, WIDTH - 100, 120), border_radius=10)
        pygame.draw.rect(screen, NEON_BLUE, (50, 140, WIDTH - 100, 120), width=1, border_radius=10)
        
        sit_surf = self.question_font.render(current_quiz["situation"], True, NEON_YELLOW)
        screen.blit(sit_surf, (80, 160))
        
        quest_surf = self.question_font.render(current_quiz["question"], True, WHITE)
        screen.blit(quest_surf, (80, 210))
        
        # 4. 보기 상자 그리기 (Option Cards)
        for idx, option in enumerate(current_quiz["options"]):
            card_y = 290 + idx * 110
            card_height = 90
            
            # 마우스 포인터 감지 혹은 디폴트 디자인
            bg_color = (20, 20, 25)
            border_color = NEON_BLUE
            
            pygame.draw.rect(screen, bg_color, (50, card_y, WIDTH - 100, card_height), border_radius=10)
            pygame.draw.rect(screen, border_color, (50, card_y, WIDTH - 100, card_height), width=2, border_radius=10)
            
            # 보기 텍스트 그리기
            opt_surf = self.option_font.render(option, True, WHITE)
            screen.blit(opt_surf, (80, card_y + (card_height - opt_surf.get_height()) // 2))
            
        # 5. 가이드 메시지 (Guide Message)
        guide_surf = self.info_font.render("키보드의 숫자 키 (1, 2, 3)를 눌러 알맞은 행동을 선택하세요.", True, (150, 150, 180))
        screen.blit(guide_surf, (50, HEIGHT - 50))
        
        # 6. 피드백 연출 오버레이 (Feedback overlay)
        if self.feedback_timer > 0:
            # 반투명 어두운 오버레이 깔기 (semi-transparent overlay)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            # 피드백 박스 (Feedback Panel)
            panel_w, panel_h = 700, 350
            panel_x = (WIDTH - panel_w) // 2
            panel_y = (HEIGHT - panel_h) // 2
            pygame.draw.rect(screen, DARK_GRAY, (panel_x, panel_y, panel_w, panel_h), border_radius=20)
            pygame.draw.rect(screen, self.feedback_color, (panel_x, panel_y, panel_w, panel_h), width=3, border_radius=20)
            
            # 결과 텍스트
            res_surf = self.feedback_font.render(self.feedback_text, True, self.feedback_color)
            screen.blit(res_surf, res_surf.get_rect(center=(WIDTH // 2, panel_y + 60)))
            
            # 틀렸을 때 상세한 오답 원인 제공 (Multilined feedback)
            if self.is_failed:
                reason_intro_surf = self.option_font.render("[오답 피드백 및 고증 정보]", True, NEON_YELLOW)
                screen.blit(reason_intro_surf, (panel_x + 50, panel_y + 110))
                
                # 긴 원인 텍스트 줄바꿈 렌더링
                words = self.fail_reason.split(' ')
                lines = []
                current_line = ""
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    test_surf = self.info_font.render(test_line, True, WHITE)
                    if test_surf.get_width() > panel_w - 100:
                        lines.append(current_line)
                        current_line = word
                    else:
                        current_line = test_line
                if current_line:
                    lines.append(current_line)
                    
                for l_idx, line in enumerate(lines):
                    line_surf = self.info_font.render(line, True, WHITE)
                    screen.blit(line_surf, (panel_x + 50, panel_y + 145 + l_idx * 28))
