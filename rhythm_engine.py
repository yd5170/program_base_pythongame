# 두쫀쿠 박자 판정 및 점수 로직

import time
from config import BPM

class RhythmEngine:
    def __init__(self):
        self.beat_interval = 60 / BPM  # 110 BPM 기준 1박자당 간격 (약 0.545초)
        self.start_time = 0
        self.is_running = False
        
        # 판정 범위 설정 (초 단위 (seconds))
        self.PERFECT_RANGE = 0.12  # ±0.12초 이내: 퍼펙트 (PERFECT)
        self.GREAT_RANGE = 0.22    # ±0.22초 이내: 그레이트 (GREAT)
        
        # 상태 제어 변수 (State Variables)
        self.last_judged_beat = -1  # 마지막으로 판정을 내린 박자 인덱스 (index)
        self.combo = 0              # 현재 연속 콤보 수
        self.max_combo = 0          # 게임 중 달성한 최대 콤보 수

    def start(self):
        """음악 및 게임 시작 시점을 기록하고 엔진 상태를 초기화합니다."""
        self.start_time = time.time()
        self.is_running = True
        self.last_judged_beat = -1
        self.combo = 0
        self.max_combo = 0

    def get_elapsed_time(self):
        """시작 이후 경과된 시간 (elapsed time)을 초 단위로 반환합니다."""
        if not self.is_running:
            return 0.0
        return time.time() - self.start_time

    def get_current_beat_fraction(self):
        """현재 경과 시간이 몇 번째 박자 위치인지 실수(float) 형태로 반환하여 시각화에 도움을 줍니다."""
        elapsed = self.get_elapsed_time()
        return elapsed / self.beat_interval

    def get_judgment(self):
        """사용자가 누른 시점의 오차를 분석하여 판정을 수행합니다. 중복 입력을 차단합니다."""
        if not self.is_running:
            return None, 0

        current_time = time.time()
        elapsed = current_time - self.start_time
        
        # 현재 가장 가까운 박자의 인덱스 (integer index) 계산
        closest_beat = round(elapsed / self.beat_interval)
        
        # 동일한 박자에 대해 중복 입력을 시도한 경우 무시 (판정 생략)
        if closest_beat == self.last_judged_beat:
            return "DUPLICATE", 0
            
        self.last_judged_beat = closest_beat
        target_time = closest_beat * self.beat_interval
        
        # 오차(오프셋 (offset)) 계산
        offset = abs(elapsed - target_time)

        if offset <= self.PERFECT_RANGE:
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            return "PERFECT", 100
        elif offset <= self.GREAT_RANGE:
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            return "GREAT", 50
        else:
            self.combo = 0  # MISS 발생 시 콤보 초기화
            return "MISS", 0