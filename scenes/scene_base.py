# 공통 씬 베이스 클래스 (Scene Base Class)

class Scene:
    def __init__(self, game):
        """
        씬 생성자 (Scene constructor)
        :param game: DujjonkuGame 인스턴스로, 전역 상태 및 씬 전환을 관리합니다.
        """
        self.game = game

    def handle_events(self, events):
        """
        이벤트 핸들러 (Event handler)
        :param events: pygame.event.get()을 통해 수집된 이벤트 리스트입니다.
        """
        pass

    def update(self):
        """
        상태 업데이트 메서드 (State update method)
        매 프레임마다 게임의 물리 및 비즈니스 로직을 갱신합니다.
        """
        pass

    def draw(self, screen):
        """
        화면 그리기 메서드 (Draw method)
        :param screen: pygame.Surface 객체로, 화면 렌더링을 지휘합니다.
        """
        pass
