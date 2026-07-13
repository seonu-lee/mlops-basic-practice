## 09. docker-compose.yml 개념 정리

### 왜 필요한가

지금까지는 `Dockerfile` 하나로 MLflow(또는 학습 환경) 컨테이너 하나만 띄웠지만, 이제는 **Airflow(웹서버+스케줄러+DB)**와 **MLflow**를 동시에 띄워야 합니다. 컨테이너가 여러 개로 늘어나면 `docker run` 명령어를 하나씩 치는 게 아니라, `docker-compose.yml` 파일 하나에 "어떤 컨테이너들을 어떻게 띄울지" 정의해두고 `docker compose up` 한 줄로 전부 실행하는 게 표준적인 방법입니다.

### 이번 구성에 들어갈 서비스

- **postgres**: Airflow가 태스크 상태, DAG 실행 기록 등을 저장하는 메타데이터 DB (Airflow는 SQLite로도 되지만 LocalExecutor 이상을 쓰려면 Postgres가 필요합니다)
- **airflow-init**: Airflow DB 초기화 및 관리자 계정 생성을 1회만 수행하는 서비스
- **airflow-webserver**: `localhost:8080`에서 볼 수 있는 UI
- **airflow-scheduler**: DAG를 실제로 스케줄링/실행하는 백그라운드 프로세스
- **mlflow**: `localhost:5000`에서 볼 수 있는 실험 추적 서버

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 5s
      retries: 5

  airflow-init:
    image: apache/airflow:2.9.3
    depends_on:
      - postgres
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    entrypoint: /bin/bash
    command:
      - -c
      - |
        airflow db init
        airflow users create \
          --username admin --password admin \
          --firstname Admin --lastname User \
          --role Admin --email admin@example.com

  airflow-webserver:
    image: apache/airflow:2.9.3
    depends_on:
      - airflow-init
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    volumes:
      - ./dags:/opt/airflow/dags
      - ./ml:/opt/airflow/ml
    ports:
      - "8080:8080"
    command: webserver

  airflow-scheduler:
    image: apache/airflow:2.9.3
    depends_on:
      - airflow-init
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    volumes:
      - ./dags:/opt/airflow/dags
      - ./ml:/opt/airflow/ml
    command: scheduler

  mlflow:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./mlruns:/mlflow/mlruns
    command: mlflow server --host 0.0.0.0 --backend-store-uri /mlflow/mlruns

volumes:
  postgres-db-volume:
```

### 이번 단계에서 새로 등장하는 개념

| 개념 | 설명 |
|---|---|
| `depends_on` | 서비스 시작 순서 지정 (postgres → airflow-init → webserver/scheduler) |
| `volumes` (named volume) | `postgres-db-volume`처럼 컨테이너 삭제 후에도 DB 데이터를 유지 |
| `volumes` (bind mount) | `./dags:/opt/airflow/dags`처럼 로컬 폴더를 컨테이너 안 경로에 실시간 연결 |
| `healthcheck` | postgres가 완전히 켜졌는지 확인 후 다음 서비스 시작 |
| `entrypoint`/`command` | 컨테이너가 시작할 때 실행할 명령어 지정 |

### 다음에 할 일

1. 레포 루트에 위 내용으로 `docker-compose.yml` 생성
2. `dags/` 폴더 생성 (비어있어도 OK, 3주차에 채울 예정)
3. `docker compose up -d` 실행해서 5개 컨테이너(postgres, airflow-init, webserver, scheduler, mlflow)가 뜨는지 확인

