# MLflow UI 확인하기

```markdown
지금까지 쌓인 것:

mlruns 폴더 안에 run 3개(n_estimators=50, 100, 200)가 
각각의 파라미터, accuracy, 모델 파일과 함께 저장되어 있음

이제 할 일:
이 기록들을 웹 브라우저 화면에서 표로 비교해보는 것
```

```markdown
mlflow ui 명령어란?

- 로컬에 저장된 mlruns 폴더를 읽어서
  웹 서버를 하나 띄워주는 명령어

- 이 서버에 브라우저로 접속하면
  run들을 리스트로, 또는 나란히 비교하는 화면을 볼 수 있음

실행 위치:
mlops-basic-practice 폴더 안 (mlruns 폴더가 있는 바로 그 위치)
cd C:\Users\seonu\Documents\mlops-basic-practice
```

```markdown
주의: 이번 명령어는 컨테이너 안에서가 아니라
"내 컴퓨터(로컬)"에서 직접 실행합니다

이유:
- mlruns 폴더가 이미 로컬에 저장되어 있으니
- 굳이 Docker 컨테이너를 또 띄울 필요 없이
  로컬에 설치된(또는 설치할) mlflow 패키지로 바로 UI를 열면 됨
```

```powershell
mlflow ui
```

```markdown
만약 "mlflow 명령어를 찾을 수 없다"는 에러가 뜨면:

로컬 컴퓨터에는 아직 mlflow 패키지가 설치되어 있지 않은 상태일 수 있음
(지금까지는 컨테이너 안에서만 mlflow를 썼기 때문)

이 경우 아래 명령어로 로컬에 mlflow만 간단히 설치하면 됨
```

```powershell
pip install mlflow
```

# MLflow 최신 버전 filesystem 에러 원인

```markdown
에러 원인:

로컬에 새로 설치된 mlflow 버전은 3.14.0인데,
이 최신 버전부터는 filesystem 방식(./mlruns 폴더를 직접 읽는 방식)이
"유지보수 모드"로 바뀌면서 기본적으로 막혀 있음

에러 메시지에도 나와 있듯이, 두 가지 중 하나가 필요함:
1. DB 기반(sqlite)으로 전환
2. MLFLOW_ALLOW_FILE_STORE=true 옵션을 켜서 파일 시스템 방식 유지
```

```markdown
버전 차이가 원인인 이유:

컨테이너 안에서는 mlflow 2.14.1을 쓰고 있어서 이 문제가 없었음
방금 로컬에 pip install mlflow로 설치된 건 최신 버전(3.14.0)이라
동작 방식 자체가 달라진 것
```

```markdown
가장 간단한 해결책:

MLFLOW_ALLOW_FILE_STORE=true 환경변수를 설정한 뒤 mlflow ui를 실행
```

```powershell
$env:MLFLOW_ALLOW_FILE_STORE="true"
mlflow ui
```

```markdown
mlflow ui 실행 후 나타나는 결과:

콘솔에 아래와 비슷한 줄이 출력됨
Listening at: http://127.0.0.1:5000

이 주소를 브라우저 주소창에 그대로 입력해서 접속
```

```markdown
브라우저에서 확인할 것:

1. 왼쪽에 "iris-classification"이라는 experiment 이름이 보이는지
2. 그 안에 run이 3개(50, 100, 200) 나열되어 있는지
3. run들을 체크박스로 선택해서 "Compare" 버튼 누르면
   accuracy를 나란히 비교하는 화면이 뜨는지

→ 이 비교 화면을 캡처해서 mlflow-ui.png로 저장
```

