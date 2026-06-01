# 🏥 두 손으로 쫀득하게 CPR (두쫀쿠)
> **의학적 고증(110BPM)과 게임 메커니즘을 결합한 Python Pygame 기반 리듬 교육 게임 (Rhythm Game)**

![Language-Python](https://img.shields.io/badge/Language-Python%203.11-blue?style=for-the-badge&logo=python)
![Library-Pygame](https://img.shields.io/badge/Library-Pygame%202.5-green?style=for-the-badge&logo=pygame)
![Theme-Cyberpunk](https://img.shields.io/badge/Theme-Cyberpunk%20Dark-magenta?style=for-the-badge)

---

## 📋 프로젝트 요약 (Summary)
"내 앞의 사람이 갑자기 쓰러졌을 때, 우리는 무엇을 할 수 있는가?"  
이 프로젝트는 응급 상황에서 생명을 살리는 가장 핵심적인 역량인 **정확한 박자의 가슴 압박**을 게임을 통해 몸으로 자연스럽게 체득할 수 있도록 설계된 파이썬 교육 리듬 게임입니다.

---

## 📺 게임 플레이 시연 및 비주얼 (Demo & Visual)

<p align="center">
  <a href="https://github.com/yd5170/program_base_pythongame/raw/main/assets/images/cpr_demo.mp4">
    <img src="https://github.com/yd5170/program_base_pythongame/raw/main/assets/images/bg_title.png" width="90%" alt="bg_title">
  </a>
</p>

<p align="center">
  💡 <b>[위 타이틀 스크린샷 이미지를 클릭하면 쫀득한 CPR 시연 동영상을 바로 다운로드 및 새 창에서 감상하실 수 있습니다!]</b>
</p>

---

## 🛠 사용 기술 및 개발 환경 (Tech Stack & Environment)
- **Language:** Python 3.11.9
- **Graphics & Sound:** Pygame 2.5.2, Pillow
- **Editor:** Visual Studio Code

---

## 💻 파이썬 기술 활용 및 설계 역량 (Core Skills)

### 1. 관심사 분리(SoC, Separation of Concerns) 및 유지보수 효율화
- **`config.py`:** 모든 게임 설정(BPM, 판정 오차 범위, 네온 컬러 팔레트)을 중앙 집중화하여 코드 내 하드코딩(hard-coding)을 완벽히 배제했습니다.
- **`scenes/` 폴더:** 각 화면(Title, Scenario, Rhythm, Result)을 독립 클래스로 모듈화하고 관리하여 구조화된 객체지향 아키텍처(Object-Oriented Architecture)를 구축했습니다.

### 2. 고정밀 박자 판정 알고리즘 (`rhythm_engine.py`)
- `time.time()`을 활용해 밀리초 단위의 정밀 타임스탬프(timestamp)를 획득하고 연산합니다.
- `closest_beat` 연산을 통해 가장 인접한 타깃 비트와의 시간 오차(Offset)를 계산하여 PERFECT / GREAT / MISS 등급을 부여합니다.
- 동일 비트 내 중복 입력 방어 로직(last_judged_beat 추적)을 구현하여 판정 시스템의 신뢰도와 정확성을 대폭 높였습니다.

### 3. 동적 씬 매니지먼트 및 이벤트 위임 (`main.py`)
- 메인 루프에서 전역 상태 변화에 따라 씬 객체를 자유롭게 교체하는 **상태 패턴(State Pattern)**을 구현했습니다.
- 전역 이벤트를 현재 활성화된 씬으로 전달(Delegate)하는 이벤트 위임 구조를 채택하여 각 스테이지별 독립 로직이 독립적으로 작동하도록 설계했습니다.

---

## 📂 파일 구조 명세 (Directory Layout)
- **[main.py](file:///c:/Users/yd517/Desktop/Project_base_python%20game/CPR_Project-main/main.py):** 게임 전체 흐름을 지휘하는 핵심 씬 매니저 및 이벤트 루프 엔진
- **[config.py](file:///c:/Users/yd517/Desktop/Project_base_python%20game/CPR_Project-main/config.py):** 의학적 고증 데이터 및 해상도, 네온 컬러 전역 상수 관리
- **[rhythm_engine.py](file:///c:/Users/yd517/Desktop/Project_base_python%20game/CPR_Project-main/rhythm_engine.py):** 박자 오차 계산 및 등급 판정 핵심 알고리즘
- **[test_logic.py](file:///c:/Users/yd517/Desktop/Project_base_python%20game/CPR_Project-main/test_logic.py):** 가슴 가압 및 텍스트 렌더링 선행 검증용 프로토타입 스크립트
- **[scenes/](file:///c:/Users/yd517/Desktop/Project_base_python%20game/CPR_Project-main/scenes/):** 타이틀, 상황 대처 퀴즈, 가수가압 리듬, 결과 씬이 상속 구현된 클래스 모음

---

## 🎮 주요 기능 (Main Features)
- **Stage 1 (Scenario):** 상황 판단 의식 확인 ➔ 구조 요청 ➔ 호흡 관찰 3단계 분기 선택 로직 (오답 시 전문 고증 의학 정보 피드백을 출력하며 즉시 실패 엔딩으로 연결)
- **Stage 2 (Rhythm):** 의학적 고증 110BPM에 정확히 맞춘 낙하 노트 타격 및 가슴 압박 모델 찌그러짐 수축-이완 애니메이션
- **AED FEVER TIME:** 15콤보(combo) 달성 시 3초간 비전 경고창과 함께 발동하는 무제한 스페이스바 난타 연타 이벤트 보너스 모드
- **아이템 및 체력 게이지:** 8비트 주기로 날아오는 핑크 하트 노트를 성공적으로 타격하면 깎인 체력(HP)을 회복하는 아이템 시스템

---

## 🛠️ Git 명령어 파일별 정밀 업로드 (Commit Log Guide)
각 파일별 역할에 맞는 독립적인 커밋 메시지를 작성하여 저장소의 전문성을 향상시키는 최종 커밋 가이드라인입니다.

```bash
# 1. 깃 초기화 및 원격 저장소 연결
git init
git remote add origin https://github.com/yd5170/program_base_pythongame.git

# 2. 파일별 역할에 맞는 전문적인 커밋 메시지 작성
git add config.py
git commit -m "chore: 의학 고증(110BPM) 및 네온 테마 전역 상수 구조화 (config.py)"

git add main.py
git commit -m "feat: 상태 패턴 기반 동적 씬 매니저 및 이벤트 위임 아키텍처 구축 (main.py)"

git add rhythm_engine.py
git commit -m "feat: 타임스탬프 기반 정밀 박자 판정 및 중복 입력 방지 엔진 구현 (rhythm_engine.py)"

git add test_logic.py
git commit -m "test: 핵심 로직(압박 판정) 검증을 위한 선행 프로토타입 개발 (test_logic.py)"

git add scenes/
git commit -m "feat: 화면별 독립적 클래스 모듈화 및 시나리오 분기 로직 개발 (scenes/)"

git add README.md
git commit -m "docs: 파이썬 기초 및 응용 역량 중심의 프로젝트 명세서 작성 (README.md)"

# 3. 깃허브로 최종 전송
git branch -M main
git push -u origin main
```
