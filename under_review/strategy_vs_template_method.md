# Strategy vs Template Method

둘 다 **행동을 교체**하는 패턴이지만, 교체 방식이 다르다. 조합(Strategy) vs 상속(Template Method).

## 핵심 차이

| 구분 | Strategy | Template Method |
|------|----------|-----------------|
| **교체 방식** | 조합 (외부에서 주입) | 상속 (하위 클래스가 오버라이드) |
| **교체 단위** | 알고리즘 전체 | 알고리즘의 특정 단계 |
| **런타임 교체** | 가능 (객체 교체) | 불가능 (클래스가 정해짐) |
| **흐름 제어** | 클라이언트가 결정 | 상위 클래스가 결정 (고정) |

## 요리로 비유하면

```
Strategy        = 배달 앱. 치킨/피자/중식 중 원하는 걸 고르면 해당 가게가 알아서 전체를 처리.
                  "전체 요리 방식"을 통째로 교체

Template Method = 레시피. "재료 준비 → 조리 → 담기" 순서는 고정.
                  같은 레시피로 재료만 바꾸면 소고기 스테이크/연어 스테이크가 됨.
                  "특정 단계"만 교체
```

## 판단 기준

```
바꾸고 싶은 게 뭔가?
├── 알고리즘 전체를 통째로 교체 → Strategy
│   (예: 정렬 방식을 버블/퀵/머지 중 선택)
└── 전체 흐름은 고정, 특정 단계만 교체 → Template Method
    (예: 데이터 파이프라인에서 read/transform 단계만 교체)

런타임에 바꿔야 하나?
├── YES → Strategy (객체를 갈아끼우면 됨)
└── NO → Template Method도 가능
```

## 코드로 보는 차이

```python
# Strategy: 알고리즘 전체를 외부에서 주입
class Context:
    def __init__(self, strategy: Strategy):
        self._strategy = strategy  # 런타임에 교체 가능!

    def execute(self):
        self._strategy.do_work()  # 전체를 위임

# Template Method: 흐름은 고정, 단계만 오버라이드
class DataPipeline(ABC):
    def run(self):  # 이 순서는 바꿀 수 없음!
        data = self.read()        # 하위 클래스가 구현
        result = self.transform(data)  # 하위 클래스가 구현
        self.save(result)         # 하위 클래스가 구현
```

## state_vs_strategy.md도 참고

State와 Strategy의 차이는 `project_knowledge/state_vs_strategy.md` 참고.
