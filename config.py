# 두쫀쿠 모든 설정값 및 경로 관리

import pygame
import os

# 1. 화면 및 게임 기본 설정 (Screen & Game Setup)
WIDTH, HEIGHT = 1024, 768  # 1024x1024 대신 표준 4:3 비율인 1024x768로 설정하여 씬 렌더링 최적화
FPS = 60

# 2. 색상 설정 (Color Palette - Neon Theme)
WHITE = (255, 255, 255)
BLACK = (10, 10, 15)       # 약간 푸른빛이 도는 세련된 검은색 (cyberpunk black)
DARK_GRAY = (30, 30, 40)   # 컴포넌트 배경용 어두운 회색
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 50)

# 네온 컬러 (Neon Colors)
NEON_PINK = (255, 0, 127)    # 피버 및 생명력 강조용 분홍색
NEON_BLUE = (0, 243, 255)    # UI 가이드 및 하이라이트용 하늘색
NEON_GREEN = (57, 255, 20)   # Perfect 판정 및 성공 상태 초록색
NEON_YELLOW = (255, 234, 0)  # Great 판정 및 경고 노란색
NEON_RED = (255, 7, 58)      # Miss 판정 및 실패 상태 빨간색

# 3. 의학적 고증 및 게임 규칙 설정 (Medical Spec & Game Rules)
BPM = 110                  # 심폐소생술 표준 속도인 110 BPM (가슴압박 속도)
TIMER_LIMIT = 30           # 제한 시간 (30초)
MAX_HP = 5                 # 최대 생명력 (하트 수)
PASS_SCORE = 2000          # 클리어 기준 합격 점수
FEVER_COMBO = 15           # 피버 타임 진입을 위한 최소 콤보 수
FEVER_DURATION = 3000      # 피버 타임 지속 시간 (3초 = 3000ms)

# 4. 경로 설정 (Path Configuration)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(BASE_PATH, "assets", "images")
SND_PATH = os.path.join(BASE_PATH, "assets", "sounds")