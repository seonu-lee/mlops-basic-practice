# Docker + MLflow 하루 미니 실습 계획


## 실습 목표
Docker로 실행 환경을 고정하고, MLflow로 간단한 분류 모델의 
실험(파라미터·메트릭·모델)을 기록·비교하는 흐름을 하루 안에 경험한다.

**최종 산출물**: mlops-basic-practice 레포 (Dockerfile, train.py, README, 스크린샷 2장)

---

## 프로젝트 구조 확정

```markdown
mlops-basic-practice/
├── Dockerfile
├── requirements.txt
├── train.py
├── README.md
└── screenshots/
    ├── mlflow-ui.png
    └── docker-running.png
```

---

## 시간대별 흐름 

| 시간 | 단계 | 내용 |
|---|---|---|
| 1시간 | 환경 이해 | Docker 기본 개념(이미지/컨테이너) + MLflow 역할 이해 |
| 1시간 | requirements.txt & Dockerfile 작성 | mlflow, scikit-learn, pandas 설치 정의 |
| 30분 | 이미지 빌드 & 컨테이너 실행 | docker build, docker run 테스트 |
| 1시간 | train.py 작성 | Iris 분류 + mlflow.log_param/metric/model |
| 1시간 | 실험 2~3회 반복 | 하이퍼파라미터 바꿔가며 run 기록 |
| 30분 | MLflow UI 확인 | 브라우저에서 run 비교, 스크린샷 촬영 |
| 1시간 | README 작성 & 정리 | 실습 요약, 스크린샷 삽입, 회고 한 줄 |


---

## 단계별 상세 체크리스트

### 1단계: requirements.txt
```markdown
- mlflow, scikit-learn, pandas 버전 명시 (버전 고정 여부는 선택)
- 이 파일이 왜 필요한지: Dockerfile이 이 목록을 읽어서 
  컨테이너 안에 동일한 패키지를 설치하게 됨
```

### 2단계: Dockerfile
```markdown
- 베이스 이미지 선택 (python:3.x-slim 계열 추천 - 가볍고 빠름)
- 작업 디렉토리 설정
- requirements.txt 복사 → 설치
- train.py 복사
- 실행 명령 정의
```

### 3단계: 이미지 빌드 & 컨테이너 실행
```markdown
- docker build로 이미지 생성
- docker run으로 컨테이너 실행해서 정상 동작 확인
- 이 시점에 docker-running.png 스크린샷 하나 찍어두기
```

### 4단계: train.py
```markdown
- 데이터 로드 (Iris - sklearn 내장 데이터셋이라 다운로드 불필요)
- train_test_split
- 분류 모델 학습 (RandomForest 등 간단한 것)
- mlflow.log_param() - 하이퍼파라미터 기록
- mlflow.log_metric() - accuracy 등 기록
- mlflow.sklearn.log_model() - 모델 아티팩트 저장
```

+ [윈도우 Docker Desktop 설치 가이드](https://hianna.tistory.com/1211)

### 5단계: 실험 반복
```markdown
- 하이퍼파라미터 1개만 바꿔가며 2~3번 실행
  (예: n_estimators를 50 → 100 → 200)
- 매 실행마다 MLflow에 별도 run으로 기록됨
```

### 6단계: MLflow UI
```markdown
- mlflow ui (또는 mlflow server) 실행
- 브라우저에서 localhost 접속
- run들 비교 화면 캡처 → mlflow-ui.png
```

### 7단계: README.md
```markdown
- 실습 목적 1~2줄
- 프로젝트 구조
- 실행 방법 (docker build → docker run 순서)
- 결과 요약 (스크린샷 삽입)
- 회고: "Docker로 MLflow 실험 환경을 구축하고, 
  간단한 모델 학습 결과를 MLflow로 추적하는 실습을 진행했습니다."
```

