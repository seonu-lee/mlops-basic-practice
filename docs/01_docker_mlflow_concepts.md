# Docker + MLflow 기본 개념 정리

> mlops-basic-practice 실습 - 1단계: 환경 이해

---

## 1. Docker가 왜 필요한가?

```markdown
문제 상황:
"내 컴퓨터에서는 됐는데, 다른 컴퓨터에서는 안 돼요"

원인:
- Python 버전이 다름 (3.9 vs 3.11)
- 설치된 라이브러리 버전이 다름 (scikit-learn 1.2 vs 1.4)
- OS 환경이 다름 (Mac vs Windows vs Linux)

Docker의 해결 방식:
"실행 환경 전체를 하나의 상자(컨테이너)에 포장해서,
 어디서 열어도 100% 똑같이 동작하게 만든다"
```

---

## 2. 핵심 개념 3가지

### 2-1. 이미지(Image) vs 컨테이너(Container)

```markdown
이미지(Image)
- 실행 환경의 "설계도" 또는 "스냅샷"
- 여기엔 Python, 설치된 라이브러리, 내 코드 파일이 다 들어있음
- 한 번 만들면 수정되지 않음 (읽기 전용)

컨테이너(Container)
- 이미지를 실제로 "실행시킨 상태"
- 이미지 = 붕어빵 틀, 컨테이너 = 실제로 구워진 붕어빵
- 하나의 이미지로 컨테이너를 여러 개 띄울 수도 있음
```

### 2-2. Dockerfile

```markdown
Dockerfile이란?
- "이미지를 어떻게 만들지"에 대한 레시피(설명서)
- 이 파일에 적힌 순서대로 명령어가 실행되면서 이미지가 만들어짐

비유:
Dockerfile = 요리 레시피
docker build = 레시피대로 요리해서 완성한 음식 (이미지)
docker run = 완성된 음식을 실제로 먹는 행위 (컨테이너 실행)
```

### 2-3. 이번 실습에서 Docker의 역할

```markdown
mlops-basic-practice 프로젝트에서 Docker는:

1. Python 특정 버전 고정
2. mlflow, scikit-learn, pandas를 정해진 버전으로 설치
3. train.py를 이 환경 안에서 실행

→ 즉, "이 컨테이너를 실행하면 무조건 같은 결과가 나온다"는 
   재현성(reproducibility)을 보장하는 역할
```

---

## 3. MLflow가 왜 필요한가?

```markdown
문제 상황:
모델을 학습시키다 보면 이런 게 반복됨:

시도 1: n_estimators=50  → accuracy 0.91
시도 2: n_estimators=100 → accuracy 0.94
시도 3: n_estimators=200 → accuracy 0.93

→ 노트북 파일을 여러 개 만들거나, 엑셀에 손으로 기록하거나,
   심지어 어떤 설정으로 어떤 결과가 나왔는지 까먹기도 함

MLflow의 해결 방식:
"실험(run)마다 파라미터·성능·모델 파일을 자동으로 기록하고,
 나중에 웹 화면에서 비교할 수 있게 해준다"
```

---

## 4. 핵심 개념 3가지

### 4-1. Run

```markdown
Run이란?
- "한 번의 실험 시도" 단위
- 코드를 한 번 실행할 때마다 run이 하나 생김
- 각 run은 고유 ID를 가지고, 그 안에 파라미터/메트릭/모델이 기록됨

예시:
train.py를 3번 실행 = run이 3개 생김
```

### 4-2. 기록되는 3가지 요소

```markdown
1. Parameter (파라미터)
   - 내가 설정한 입력값
   - 예: n_estimators=100, max_depth=5

2. Metric (메트릭)
   - 모델의 성능 결과
   - 예: accuracy=0.94, f1_score=0.92

3. Artifact (아티팩트)
   - 학습된 모델 파일 자체, 또는 그래프 이미지 등
   - 나중에 이 모델을 다시 불러와서 쓸 수도 있음
```

### 4-3. MLflow UI

```markdown
MLflow UI란?
- 기록된 모든 run들을 웹 브라우저에서 표로 비교해볼 수 있는 화면
- "어떤 설정이 성능이 가장 좋았는지" 한눈에 파악 가능

이번 실습에서 할 일:
mlflow ui 명령어로 화면을 띄우고,
run 2~3개를 나란히 비교하는 화면을 스크린샷으로 남기기
```

---

## 5. Docker + MLflow, 두 개를 같이 쓰는 이유

```markdown
Docker  → "실행 환경"을 고정한다   (어떤 컴퓨터에서 돌려도 동일)
MLflow  → "실험 결과"를 기록한다   (어떤 설정으로 뭘 했는지 추적)

두 개를 합치면:
"동일한 환경에서, 어떤 실험을 했고 결과가 어땠는지까지
 모두 재현 가능하고 추적 가능한 상태"가 됨

→ 이게 바로 MLOps의 아주 기초적인 형태
```

---

## 6. 오늘 실습에서 사용할 최소 범위 (다시 확인)

```markdown
Docker  : 이미지 빌드 + 컨테이너 실행만
MLflow  : tracking 기능만 (배포, 모델 서빙 X)
모델    : scikit-learn 분류 모델 1개
저장소  : 로컬 파일 시스템만 (S3, 클라우드 X)
```

