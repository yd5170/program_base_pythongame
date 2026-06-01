# 두쫀쿠 씬 매니저 역할
# 전체 흐름을 제어하는 메인 실행 파일

import pygame
import sys
from config import WIDTH, HEIGHT, FPS, BLACK
from scenes.title_scene import TitleScene

class DujjonkuGame:
    def __init__(self):
        """
        두쫀쿠 게임 엔진 초기화 및 메인 매니저 설정 (Game manager setup)
        """
        pygame.init()
        
        # 1024x768 사양의 게임 창 설정 (Screen layout setting)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("두 손으로 쫀득하게 CPR (두쫀쿠) - 리듬 교육 게임")
        
        # 메트로놈 역할을 할 클록 설정 (Clock setting)
        self.clock = pygame.time.Clock()
        
        # 최초 실행 시 메인 타이틀 화면 로드
        self.current_scene = TitleScene(self)
        
    def change_scene(self, new_scene):
        """
        활성화된 씬을 새로운 씬으로 동적으로 전환합니다 (Scene transition)
        :param new_scene: 전환하여 보여줄 Scene 인스턴스
        """
        self.current_scene = new_scene

    def handle_events(self):
        """
        사용자의 전체 입력 이벤트를 감지하고 이를 현재 씬으로 위임합니다 (Event delegation)
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # 현재 활성화된 씬에 이벤트를 전달하여 세부 로직을 수행시킵니다.
        self.current_scene.handle_events(events)

    def update(self):
        """
        현재 활성화된 씬의 물리 상태 및 변수들을 갱신합니다 (State update delegation)
        """
        self.current_scene.update()

    def draw(self):
        """
        화면 백버퍼를 검은색으로 밀어낸 뒤, 현재 씬의 렌더링 함수를 가동시킵니다 (Drawing delegation)
        """
        self.screen.fill(BLACK)
        self.current_scene.draw(self.screen)
        pygame.display.flip()  # 프레임 교체로 화면 갱신 (Double buffering)

    def run(self):
        """
        게임의 메인 게임 루프 (Main Game Loop)를 초당 60프레임 속도로 동작시킵니다.
        """
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = DujjonkuGame()
    game.run()