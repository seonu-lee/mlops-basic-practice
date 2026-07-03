# requirements.txt 작성 — 개념 정리

```markdown
requirements.txt란?
- "이 프로젝트를 실행하려면 어떤 패키지가 필요한지" 적어두는 목록 파일
- Dockerfile이 이 파일을 읽어서, 컨테이너 안에 똑같이 설치함

왜 따로 파일로 분리하나?
- 설치할 패키지 목록과 Dockerfile(환경 설정)을 분리해두면
  나중에 패키지만 추가/변경할 때 Dockerfile을 건드릴 필요 없음
```

```markdown
이번 실습에 필요한 패키지 3가지:

1. mlflow        → 실험 추적 (run 기록, UI)
2. scikit-learn  → 분류 모델 학습, Iris 데이터셋 포함
3. pandas        → 데이터 다루기 (필수는 아니지만 습관상 같이 씀)
```

```markdown
버전을 명시할지 말지 선택지:

옵션 A) 버전 고정 안 함 → mlflow, scikit-learn, pandas
   - 장점: 간단함
   - 단점: 나중에 실행할 때 버전이 달라질 수 있음 (재현성 ↓)

옵션 B) 버전 명시 → mlflow==2.x.x 처럼 적음
   - 장점: 언제 실행해도 동일한 환경 보장 (Docker 쓰는 이유와 부합)
   - 단점: 버전 확인하는 절차가 하나 더 필요함

→ 하루 실습 + 재현성 연습이 목적이니 옵션 B(버전 명시) 추천
```

---

# requirements.txt 파일 내용

```markdown
아래는 오늘 실습에 필요한 패키지 3가지를 버전까지 명시한 requirements.txt입니다.
```

```txt
mlflow==2.14.1
scikit-learn==1.5.0
pandas==2.2.2
```

```markdown
각 줄이 하는 역할:

mlflow==2.14.1        → 실험(run) 기록 + UI 제공
scikit-learn==1.5.0   → Iris 데이터셋 + 분류 모델(RandomForest 등)
pandas==2.2.2         → 데이터프레임 형태로 다루기 편하게

버전 표기 방식(==)의 의미:
"==" 는 "정확히 이 버전만 설치해라"는 뜻
(>= 를 쓰면 "이 버전 이상이면 다 허용"이라 재현성이 떨어짐)
```