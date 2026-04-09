# Factory vs Builder

둘 다 **객체 생성**을 다루는 패턴이지만, 해결하는 문제가 다르다.

## 핵심 차이

| 구분 | Factory | Builder |
|------|---------|---------|
| **해결하는 문제** | "어떤 종류를 만들지" 결정 | "어떻게 조립할지" 단계적 구성 |
| **결과물** | 한 번에 완성된 객체 반환 | 단계별로 조립 후 완성 |
| **선택 기준** | 조건/타입에 따라 다른 클래스 선택 | 파라미터가 많거나 선택적 옵션이 많을 때 |
| **호출 방식** | `create("email")` → 즉시 반환 | `.table().select().where().build()` |

## 식당으로 비유하면

```
Factory = 메뉴판에서 고르기. "아메리카노 주세요" → 바로 나옴
          어떤 음료를 만들지 선택하는 것이 핵심

Builder = 서브웨이 주문. 빵 → 고기 → 야채 → 소스를 단계별로 선택
          같은 과정으로 완전히 다른 샌드위치가 나옴
```

## 판단 기준

```
객체 생성에서 뭐가 복잡한가?
├── "어떤 종류를 만들지" 분기가 복잡 → Factory
│   (예: 채널별로 다른 알림 객체 생성)
└── "파라미터/옵션 조합"이 복잡 → Builder
    (예: SQL 쿼리의 SELECT, WHERE, ORDER BY, LIMIT 조합)
```

## 코드로 보는 차이

```python
# Factory: 조건에 따라 다른 클래스를 선택
def create_notification(channel: str) -> Notification:
    factories = {"email": EmailNotification, "slack": SlackNotification}
    return factories[channel]()  # 한 번에 완성

# Builder: 단계별로 조립
query = (
    QueryBuilder()
    .table("users")         # 1단계
    .select("name", "email")  # 2단계
    .where("age > 20")      # 3단계 (선택)
    .order("name")          # 4단계 (선택)
    .build()                # 완성!
)
```

## 함께 쓰는 경우

Factory가 "어떤 Builder를 쓸지" 결정하고, Builder가 "어떻게 조립할지" 처리하는 조합도 가능하다. 예: 지역(NY/Chicago)에 따라 다른 PizzaBuilder를 선택하고, 각 Builder가 피자를 단계별로 조립.
