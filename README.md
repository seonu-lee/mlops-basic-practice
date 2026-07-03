# mlops-basic-practice

Docker로 실행 환경을 고정하고, MLflow로 간단한 분류 모델의 실험(파라미터·메트릭·모델)을
기록·비교하는 흐름을 하루 동안 실습한 프로젝트입니다.

## 실습 목적

- Docker: Python, scikit-learn, MLflow가 포함된 동일한 실행 환경 구성
- MLflow: run별로 파라미터, 정확도, 모델 파일을 저장하고 UI에서 비교

## 프로젝트 구조

```
mlops-basic-practice/
├── Dockerfile
├── requirements.txt
├── train.py
├── README.md
└── screenshots/
    ├── mlflow-ui.png
    └── docker-running.png
```

## 사용 기술

- Python 3.10
- scikit-learn (RandomForestClassifier, Iris 데이터셋)
- MLflow (실험 추적: log_param, log_metric, log_model)
- Docker (실행 환경 컨테이너화)

## 실행 방법

### 1. 이미지 빌드

```powershell
docker build -t mlops-practice .
```

### 2. 컨테이너 실행 (볼륨 마운트로 mlruns 로컬 저장)

```powershell
docker run -v ${PWD}/mlruns:/app/mlruns mlops-practice
```

### 3. 하이퍼파라미터 변경 후 반복 실행

train.py 상단의 `n_estimators` 값을 50 → 100 → 200으로 바꿔가며
위 build/run 과정을 반복하면, 매 실행마다 MLflow에 새로운 run이 기록됩니다.

### 4. MLflow UI로 결과 비교

```powershell
$env:MLFLOW_ALLOW_FILE_STORE="true"
mlflow ui
```

브라우저에서 `http://127.0.0.1:5000` 접속 → iris-classification experiment →
run들을 선택해 accuracy 비교 (Chart 뷰)

## 결과 요약

n_estimators 값을 50, 100, 200으로 바꿔가며 실험한 결과, 세 경우 모두
Iris 데이터셋 기준 accuracy 1.00을 기록했습니다. Iris 데이터셋은 클래스 간
경계가 뚜렷해 비교적 쉬운 분류 문제이기 때문에, 하이퍼파라미터 변화에 따른
성능 차이보다는 MLflow의 실험 기록·비교 흐름 자체를 익히는 데 집중했습니다.

| n_estimators | max_depth | accuracy |
|---|---|---|
| 50  | 3 | 1.00 |
| 100 | 3 | 1.00 |
| 200 | 3 | 1.00 |

## 스크린샷

- `screenshots/docker-running.png` : 컨테이너 실행 및 학습 로그
- `screenshots/mlflow-ui.png` : MLflow UI에서 run별 accuracy 비교 화면

## 회고

Docker로 MLflow 실험 환경을 구축하고, 간단한 분류 모델 학습 결과를
MLflow로 추적·비교하는 실습을 진행했습니다. 컨테이너 안에서 기록한 실험이
컨테이너 종료 후에도 남도록 볼륨 마운트를 적용했고, 로컬과 컨테이너의
MLflow 버전 차이로 인한 이슈(filesystem backend 제한)를 `mlflow.set_experiment()`
및 환경변수 설정으로 해결하는 과정에서 Docker와 MLflow의 동작 방식을
더 구체적으로 이해할 수 있었습니다.
