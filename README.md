# 둘리코인 기반 텔레그램 바카라 봇

## 주요 명령어
- `/시작` : 가입 및 초기 10,000 둘리코인 지급
- `/잔액` : 현재 코인 조회
- `/뱅 금액` : 뱅커에 배팅
- `/플 금액` : 플레이어에 배팅
- `/충전 사용자ID 금액` : 관리자만 사용

## 사용 방법
1. 저장소를 복사하거나 Clone합니다.
2. `ADMIN_IDS`에 본인 Telegram user_id 설정
3. `TELEGRAM_TOKEN` 환경변수에 본인 Bot Token 입력
4. `pip install -r requirements.txt` 실행
5. `python3 main.py` 또는 `python main.py`로 실행
6. `keep_alive.py`가 Flask 서버 띄워 외부 URL 제공

## 봇 유지 방법
- GoormIDE, Replit 등의 클라우드 IDE 사용 시
- 해당 URL을 UptimeRobot에 등록하면 24시간 꺼지지 않게 유지됨
