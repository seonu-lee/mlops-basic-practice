import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. 하이퍼파라미터 (실습 시 이 값만 바꿔가며 재실행)
n_estimators = 100
max_depth = 3

# 2. 데이터 불러오기
iris = load_iris()
X, y = iris.data, iris.target

# 3. train/test 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. MLflow run 시작
mlflow.set_experiment("iris-classification")

with mlflow.start_run():

    # 5. 모델 학습
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)

    # 6. 성능 평가
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # 7. MLflow에 파라미터 기록
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    # 8. MLflow에 메트릭 기록
    mlflow.log_metric("accuracy", accuracy)

    # 9. MLflow에 모델 파일 저장
    mlflow.sklearn.log_model(model, "model")

    print(f"n_estimators={n_estimators}, max_depth={max_depth} -> accuracy={accuracy:.4f}")