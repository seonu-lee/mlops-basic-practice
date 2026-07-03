# build/run 명령어 입력 위치 + 실제 명령어

```markdown
어디에 입력하나?

"터미널(Terminal)"이라는 프로그램에 입력합니다.
Dockerfile을 코드 에디터로 열어서 그 안에 입력하는 게 아니라,
별도의 "명령어를 입력하는 검은 화면" 같은 프로그램을 엽니다.

운영체제별 터미널:
- Mac         → Terminal 앱 (Spotlight 검색에서 "터미널" 검색)
- Windows     → PowerShell 또는 명령 프롬프트(cmd)
- VS Code 사용 중이면 → VS Code 안에 내장된 터미널 탭 사용 가능
  (메뉴에서 Terminal → New Terminal)
```

```markdown
입력 전에 반드시 해야 할 것: 폴더 이동

터미널을 열면 기본적으로 "홈 폴더"에서 시작됨
→ mlops-basic-practice 폴더로 직접 이동해야 함

이동하는 명령어: cd (change directory의 약자)
```

**Windows 기준 build/run 명령어**

```markdown
사용 프로그램: PowerShell
(Windows 검색창에 "PowerShell" 입력해서 실행)
```

```markdown
1단계: 폴더로 이동
```

```powershell
cd C:\Users\seonu\Documents\mlops-basic-practice
```

```markdown
2단계: 이미지 빌드
```

이 명령어는 Dockerfile을 읽어서 
Python + mlflow + scikit-learn + pandas가 설치된 이미지를 만듭니다.

```powershell
docker build -t mlops-practice .
```

빌드 중 확인할 것:
- 여러 줄의 로그가 쭉 출력됨 (패키지 설치 과정)
- 마지막 줄 근처에 "writing image" 또는 "naming to" 같은 
  완료 메시지가 뜨면 성공
- 시간은 1~3분 정도 걸릴 수 있음 (처음 빌드라 이미지 다운로드도 같이 일어남)

```markdown
3단계: 컨테이너 실행 (볼륨 마운트 포함, PowerShell 문법)
```

(${PWD}는 PowerShell 문법이고, cmd에서는 %cd%를 씀)

```powershell
docker run -v ${PWD}/mlruns:/app/mlruns mlops-practice
```

실행 후 확인할 것:
1. 콘솔에 아래와 비슷한 줄이 출력됨
   n_estimators=100, max_depth=3 -> accuracy=0.9xxx

2. mlops-basic-practice 폴더 안에 mlruns 폴더가 새로 생겼는지 확인
   (탐색기로 열어서 눈으로 확인)

3. 이 화면을 캡처 → screenshots\docker-running.png로 저장


```markdown
각 명령어 요소 설명:

docker build -t mlops-practice .
- -t mlops-practice : 이미지 이름을 "mlops-practice"로 지정
- 맨 끝의 "." : 현재 폴더를 빌드 컨텍스트로 사용

docker run -v ${PWD}/mlruns:/app/mlruns mlops-practice
- -v : 볼륨 마운트 옵션
- ${PWD}/mlruns : 현재 폴더 기준 mlruns 폴더 (호스트 쪽)
  (${PWD}는 "현재 폴더 경로"를 자동으로 가져오는 명령어)
- :/app/mlruns : 컨테이너 내부의 mlruns 폴더 (Dockerfile에서 
  WORKDIR을 /app으로 지정했으므로 컨테이너 안 경로는 /app/mlruns)
- mlops-practice : 실행할 이미지 이름

이 명령어 실행 시 일어나는 일:
1. mlops-practice 이미지로 컨테이너 실행
2. train.py 자동 실행 → 학습 진행
3. 컨테이너 내부 /app/mlruns 폴더 = 
   내 컴퓨터의 mlops-basic-practice\mlruns 폴더로 연결됨
4. 콘솔에 accuracy 결과 출력됨
```

```markdown
실행 후 확인할 것

1. PowerShell 콘솔에 아래와 비슷한 줄이 출력되는지 확인
   n_estimators=100, max_depth=3 -> accuracy=0.9xxx

2. mlops-basic-practice 폴더 안에 mlruns 폴더가 
   새로 생겼는지 탐색기에서 확인
   (생겼다면 볼륨 마운트가 정상 작동한 것)

3. 이 PowerShell 화면을 캡처해서 
   screenshots\docker-running.png 로 저장
```

```markdown
실행 순서 요약:

1. 터미널 열기
2. cd 명령어로 mlops-basic-practice 폴더로 이동
3. docker build -t mlops-practice .   실행 → 이미지 생성
4. docker run -v ... mlops-practice   실행 → 컨테이너 실행 + 학습
5. 콘솔에 accuracy 로그 확인
6. 이 화면 캡처 → docker-running.png로 저장
```

---

# mlflow.set_experiment() 개념 정리

```markdown
문제 다시 정리:

- mlflow.start_run()을 호출하면 MLflow는 기본적으로 
  "experiment ID 0번"을 찾아서 그 안에 run을 기록하려고 함

- 이 0번 experiment는 원래 mlruns 폴더가 최초로 초기화될 때 
  자동으로 생성되어야 하는데, Windows + Docker 볼륨 마운트 조합에서는
  이 초기화 과정이 제대로 완료되지 않는 경우가 있음

- 결과: "experiment 0번을 찾을 수 없다"는 에러 발생
```

```markdown
mlflow.set_experiment() 이란?

- "이 실험은 0번 기본 experiment가 아니라, 
   내가 지정한 이름의 experiment에 기록해라"라고 
   명시적으로 알려주는 함수

- 만약 그 이름의 experiment가 아직 없다면?
  → MLflow가 알아서 새로 만들어줌 (자동 생성)
  → 즉, 기존의 "0번이 미리 존재해야 한다"는 전제 자체가 사라짐
```

```markdown
코드에서 위치:

mlflow.start_run() 보다 "먼저" 호출되어야 함

흐름:
1. mlflow.set_experiment("실험이름")   ← 먼저 실행
2. with mlflow.start_run():            ← 그 다음 실행
       (기존 코드 그대로)
```

```markdown
이번 실습에 적용할 experiment 이름 (예시):

"iris-classification"

→ 이렇게 이름을 지정해두면 MLflow UI에서도
   "iris-classification"이라는 이름의 experiment로 
   run들이 깔끔하게 모여서 보임
```