# 이미지 빌드 & 컨테이너 실행 — 개념 정리

```markdown
지금까지 만든 것:
- requirements.txt (필요한 패키지 목록)
- Dockerfile (이미지 레시피)

이제 이 레시피를 실제로 "실행"해서 이미지를 만들고,
그 이미지로 컨테이너를 띄우는 단계입니다.
```

```markdown
docker build 란?

- Dockerfile에 적힌 순서대로 명령어를 실행해서
  실제 이미지(image)를 만들어내는 명령어

- 빌드가 끝나면, 내 컴퓨터에 "이미지"라는 결과물이 하나 생김
  (아직 실행된 상태는 아님 — 붕어빵 틀에서 붕어빵을 막 꺼낸 상태)
```

```markdown
docker build 명령어에 들어가는 핵심 요소 2가지

1. 이미지 이름(태그)
   - 내가 만든 이미지를 나중에 알아보기 쉽게 붙이는 이름
   - 예: mlops-practice 같은 식

2. 빌드 컨텍스트(경로)
   - Dockerfile과 관련 파일들이 있는 폴더 위치
   - 보통 "현재 폴더"를 의미하는 점(.) 하나로 표시
```

```markdown
docker run 이란?

- 빌드된 이미지를 실제로 "실행"해서 컨테이너로 만드는 명령어
- Dockerfile 마지막 줄에 적어둔 CMD(python train.py)가 
  이 시점에 자동으로 실행됨

- 즉, docker run 명령어 한 줄로:
  컨테이너가 뜨고 → train.py가 돌아가고 → 학습이 끝나면 컨테이너도 종료됨
```

```markdown
이번 실습에서 확인해야 할 것

1. docker build가 에러 없이 끝나는지
   (requirements.txt 패키지 설치가 실패하지 않는지 확인하는 단계이기도 함)

2. docker run 했을 때 train.py가 정상적으로 실행되고,
   콘솔에 학습 결과(예: accuracy 출력) 같은 로그가 찍히는지

→ 이 시점에 docker-running.png 스크린샷을 찍어두면 됩니다
   (콘솔에 컨테이너 실행 로그가 보이는 화면)
```

```markdown
주의할 점 (노베이스라면 헷갈릴 수 있는 부분)

- train.py 파일이 아직 없는 상태입니다 (다음 단계에서 작성)
- train.py 없이 빌드하면 COPY train.py . 부분에서 에러가 날 수 있으니,
  실제 빌드 테스트는 train.py를 최소한이라도 만든 뒤에 하는 게 자연스럽습니다.
- 실제 흐름상 train.py를 먼저 작성하고, 그다음에 build/run 명령어를 실습하는 게 자연스러운데 순서를 바꿔서 train.py 단계로 먼저 넘어가겠습니다.
```
---

# 이미지 빌드 & 컨테이너 실행 — 명령어 개념 정리

```markdown
이제 준비된 파일 3개:
- requirements.txt
- Dockerfile
- train.py

이 상태에서 실제로 이미지를 빌드하고 컨테이너를 실행하는 단계입니다.
```

```markdown
docker build 명령어 구조

docker build -t [이미지이름] [빌드컨텍스트경로]

- -t : 이미지에 이름(태그)을 붙이는 옵션 (tag의 약자)
- 빌드컨텍스트경로 : Dockerfile이 있는 위치
  → 보통 현재 폴더를 의미하는 "." 을 사용

실행 위치:
mlops-basic-practice/ 폴더 안에서 실행해야 함
(Dockerfile, requirements.txt, train.py가 다 이 폴더 안에 있으므로)
```

```markdown
docker run 명령어 구조

docker run [이미지이름]

- 방금 빌드한 이미지를 실제로 실행
- Dockerfile 마지막 줄의 CMD ["python", "train.py"]가 
  이 시점에 자동 실행됨
- train.py 실행 결과(accuracy 등)가 콘솔에 로그로 출력됨
```

```markdown
이번 단계에서 확인할 것 (체크리스트)

1. docker build 실행 시 에러 없이 "Successfully built" 또는 
   유사한 완료 메시지가 뜨는지
   
2. docker run 실행 시 train.py의 print문 결과
   (n_estimators=100, max_depth=3 -> accuracy=0.xxxx) 가 
   콘솔에 정상 출력되는지

3. 이 콘솔 화면을 캡처해서 docker-running.png로 저장
   (screenshots/ 폴더에 넣을 예정)
```

```markdown
주의: MLflow 기록이 저장되는 위치

- train.py 안에서 mlflow.start_run()을 쓰면
  기본적으로 컨테이너 안의 로컬 경로(mlruns/ 폴더)에 기록됨

- 문제: 컨테이너는 실행이 끝나면 사라지는 경우가 많아서
  기록된 mlruns 폴더도 같이 사라질 수 있음

- 해결 방법: 호스트(내 컴퓨터)와 컨테이너의 폴더를 연결하는
  "볼륨 마운트(volume mount)"가 필요함
  → 이 부분은 다음 개념으로 이어집니다
```
