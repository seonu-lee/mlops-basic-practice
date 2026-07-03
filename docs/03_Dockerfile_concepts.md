# Dockerfile 작성 — 개념 정리

```markdown
Dockerfile이란? (복습)
- 이미지를 만들기 위한 "레시피" 파일
- 이 안에 적힌 명령어가 위에서부터 순서대로 실행되면서
  최종적으로 하나의 이미지가 완성됨
```

```markdown
Dockerfile을 구성하는 핵심 명령어 5가지 (이번 실습 기준)

1. FROM
   - 어떤 베이스 이미지 위에서 시작할지 지정
   - 예: Python이 미리 설치된 이미지를 가져다 씀
   - 비유: 요리할 때 "빈 냄비"가 아니라 "육수가 이미 깔린 냄비"에서 시작

2. WORKDIR
   - 컨테이너 안에서 작업할 폴더 위치 지정
   - 이후 명령어들은 다 이 폴더 기준으로 실행됨
   - 비유: "이제부터 이 작업대에서 요리할게요" 선언

3. COPY
   - 내 컴퓨터(호스트)의 파일을 컨테이너 안으로 복사
   - requirements.txt, train.py 둘 다 이 명령어로 넣음

4. RUN
   - 이미지를 만드는 "시점"에 실행되는 명령어
   - 여기서 pip install로 패키지를 설치함
   - 주의: RUN은 "이미지 빌드할 때 한 번" 실행되는 것 (컨테이너 실행할 때마다 X)

5. CMD
   - 컨테이너가 "실행될 때" 자동으로 돌아가는 명령어
   - 예: python train.py 를 여기 적어두면
     컨테이너를 실행하는 순간 학습 스크립트가 자동으로 돌아감
```

```markdown
RUN vs CMD 헷갈리기 쉬운 부분 구분

RUN  → 이미지 빌드 시점 (docker build 할 때 실행)
       예: 패키지 설치

CMD  → 컨테이너 실행 시점 (docker run 할 때 실행)
       예: 학습 스크립트 실행

비유:
RUN = 요리 재료 손질하고 준비하는 과정 (미리 다 해둠)
CMD = 손님이 왔을 때 "짜잔" 하고 내놓는 최종 동작
```

```markdown
이번 실습 Dockerfile에 들어갈 흐름 순서 (미리보기)

1. Python 베이스 이미지 선택
2. 작업 폴더 지정
3. requirements.txt만 먼저 복사
4. pip install 실행 (패키지 설치)
5. train.py 복사
6. 컨테이너 실행 시 python train.py가 자동 실행되도록 설정
```

```markdown
왜 requirements.txt를 먼저 복사하고, 그 다음에 pip install을 할까?
(순서에 이유가 있는 부분)

- Docker는 각 단계를 "레이어(layer)"로 캐싱함
- train.py 코드만 수정했을 때, requirements.txt가 안 바뀌었다면
  pip install 단계는 다시 실행하지 않고 캐시를 재사용함
  → 빌드 속도가 훨씬 빨라짐

- 만약 코드와 패키지 설치를 한 번에 복사하고 설치하면
  코드를 한 글자만 고쳐도 매번 패키지를 처음부터 다시 설치하게 됨
```

---

# Dokerfile 파일 내용

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY train.py .

CMD ["python", "train.py"]
```

```markdown
각 줄이 방금 배운 개념과 어떻게 연결되는지:

FROM python:3.10-slim   → 베이스 이미지 지정
WORKDIR /app             → 컨테이너 안 작업 폴더를 /app으로 지정
COPY requirements.txt .  → requirements.txt만 먼저 복사 (캐싱 전략)
RUN pip install ...      → 빌드 시점에 패키지 설치
COPY train.py .          → 학습 스크립트 복사
CMD ["python", "train.py"] → 컨테이너 실행 시 자동으로 학습 시작
```
