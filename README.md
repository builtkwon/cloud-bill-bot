# ☁️ Cloud Bill Bot

AWS EC2 인스턴스 상태를 Discord 채널에서 실시간으로 조회할 수 있는 슬래시 명령어 기반 클라우드 어시스턴트 봇입니다.  
Discord API와 AWS SDK(Boto3)를 활용하여 간편한 인프라 모니터링을 자동화합니다.

---

## ✨ 취지

무료 플랜으로 연습하던 중 뒤늦게 비용이 발생한 것을 확인하고 눈물을 훔쳤습니다.  
그래서 비용 청구 상태를 디스코드에서 바로 확인하고 싶었습니다.  
Slack은 무겁고, 브라우저는 번거롭고, 디스코드가 열려 있길래 봇으로 만들었습니다.

---

## 📌 기능 소개 (discord 명령어)

- `/setup` : AWS Access Key, Secret Key, Region 선택 → 안전하게 암호화되어 저장
- `/status` : 현재 연결된 AWS 계정의 전체 리소스 상태 조회
- `/account` : 현재 연결된 AWS 계정 조회
- `/bill` : 현재 연결된 AWS 계정의 비용 청구 상태 조회

---

## 🛠️ 사용 기술

| 구분         | 내용                      |
|--------------|---------------------------|
| 언어         | Python 3.11+              |
| Discord API  | `discord.py` (v2.3+)      |
| AWS SDK      | `boto3`                   |
| 환경 관리    | `python-dotenv`           |
| 암호화       | `cryptography.fernet`     |

---

## 📂 프로젝트 구조

```bash
cloud-bill-bot/
├── src/
│   ├── bot.py                   # 디스코드 봇 메인 진입점
│   ├── aws_handler.py           # EC2 상태 조회 함수
│   ├── setup.py                 # 키 입력 모달
│   ├── region_view.py           # 리전 선택 드롭다운
├── utils/
│   ├── crypto.py                # 암호화/복호화 유틸리티
│   └── memory_config.py         # 서버별 구성 저장/조회
│   └── aws_client_factory.py    # 세션 정보 조회 및 리턴
├── config/                      # 서버별 키 저장 JSON
│   └── aws_keys_<guild_id>.json
├── encryption_key.key           # 암호화 키 (자동 생성)
├── .env                         # 환경 변수 (DISCORD_TOKEN)
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🚧 향후 확장 계획

- [ ] /ec2start, /ec2stop 명령어 추가
- [ ] IAM Role 기반 인증 전환
- [ ] CloudWatch 알림 연동
- [ ] Slack / Email 등 외부 채널 알림 연동
- [x] EC2 외 S3, RDS, Billing 등 자원 감시 확장

---

## ⚠️ 주의사항

- `.env`, `encryption_key.key`, `config/` 내 JSON 파일은 Git에 커밋하지 마세요
- 봇은 Discord 서버별로 EC2 정보를 분리하여 관리합니다
