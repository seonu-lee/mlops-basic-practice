# train.py 작성 — 개념 정리

```markdown
train.py가 하는 일 (전체 흐름)

1. 데이터 불러오기 (Iris 데이터셋)
2. train/test로 데이터 나누기
3. 분류 모델 학습 (RandomForest 등)
4. MLflow로 실험 기록 시작
5. 파라미터, 정확도, 모델 파일을 MLflow에 저장
```

```markdown
MLflow 관련 핵심 함수 3개 (이전 단계에서 배운 개념의 실제 사용)

1. mlflow.start_run()
   - "지금부터 하나의 run을 시작한다"는 선언
   - 이 블록 안에서 일어나는 log_param, log_metric 등이
     전부 같은 run에 묶여서 기록됨

2. mlflow.log_param(key, value)
   - 내가 설정한 하이퍼파라미터를 기록
   - 예: n_estimators 값을 기록

3. mlflow.log_metric(key, value)
   - 모델 성능 결과를 기록
   - 예: accuracy 값을 기록

4. mlflow.sklearn.log_model(model, artifact_path)
   - 학습이 끝난 모델 자체를 파일로 저장
   - 나중에 이 모델을 다시 불러와서 예측에 쓸 수 있음
```

```markdown
왜 mlflow.start_run()으로 감싸야 하나?

- start_run() 없이 log_param을 호출하면
  MLflow가 "기본 run"을 자동으로 하나 만들어서 거기 기록함
- 하지만 명시적으로 with mlflow.start_run(): 블록을 쓰면
  "이 코드 실행 = 정확히 하나의 실험"이라는 게 명확해지고,
  나중에 여러 번 실행했을 때 run들이 깔끔하게 구분됨
```

```markdown
이번 실습에서 바꿔볼 하이퍼파라미터

- n_estimators (트리 개수) 하나만 바꿔가며 3번 실행 예정
  예: 50 → 100 → 200

- 이렇게 하면 MLflow UI에서
  "n_estimators가 늘어날수록 accuracy가 어떻게 변하는지" 비교 가능
```
