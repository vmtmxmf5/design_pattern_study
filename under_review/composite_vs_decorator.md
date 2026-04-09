# Composite vs Decorator

둘 다 **재귀적으로 객체를 감싸는** 구조이지만, 감싸는 목적이 다르다.

## 핵심 차이

| 구분 | Composite | Decorator |
|------|-----------|-----------|
| **목적** | 트리 구조 표현 (부분-전체) | 기능 추가 (래핑) |
| **자식 수** | 여러 개 (N개) | 하나 (1개) |
| **관계** | 부모-자식 계층 | 감싸기 체인 |
| **연산 방향** | 재귀적으로 합산 (아래→위) | 순서대로 덧붙임 (밖→안) |

## 비유하면

```
Composite = 폴더 구조. 폴더 안에 파일과 하위 폴더가 들어감.
            "전체 크기"를 구하면 재귀적으로 합산

Decorator = 선물 포장. 선물을 리본으로 감싸고, 그걸 다시 상자에 넣고, 또 포장지로 감쌈.
            각 층이 기능(장식)을 하나씩 추가
```

## 판단 기준

```
객체를 감싸는 이유가 뭔가?
├── 여러 객체를 트리로 묶어서 일괄 처리 → Composite
│   (예: 폴더.get_size() → 모든 파일 크기 합산)
│
└── 하나의 객체에 기능을 겹겹이 추가 → Decorator
    (예: @timer @retry @log_call 순서대로 기능 추가)
```

## 구조적 차이

```python
# Composite: 자식이 여러 개 (트리 구조)
class Directory:
    def __init__(self):
        self._children = []  # File, Directory 모두 가능

    def get_size(self):
        return sum(child.get_size() for child in self._children)

# Decorator: 감싸는 대상이 하나 (체인 구조)
class TimerDecorator:
    def __init__(self, wrapped):
        self._wrapped = wrapped  # 딱 하나만 감쌈

    def execute(self):
        start = time.time()
        self._wrapped.execute()  # 원본에 위임
        print(f"소요: {time.time() - start}초")
```

## 함께 쓰는 경우

Composite 트리의 각 노드를 Decorator로 감쌀 수 있다. 예: 파일 시스템에서 특정 파일에 암호화 Decorator를 적용.
