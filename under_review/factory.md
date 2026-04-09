# Factory Pattern

## 한 줄 정의

객체를 만드는 코드를 별도로 분리하여, 클라이언트가 구체적인 클래스 이름을 몰라도 객체를 생성할 수 있게 하는 패턴. `if/else`로 `new`를 호출하던 코드를 한 곳으로 모으는 것.

## 언제 사용하는가

- **생성할 객체의 종류가 조건에 따라 달라질 때**: 여러 곳에 흩어진 `if/else` 생성 코드를 한 곳으로 모으고 싶은 경우
- **생성 방식이 바뀔 가능성이 높을 때**: 생성 로직이 바뀌어도 클라이언트 코드는 수정할 필요 없음
- **프레임워크를 만들 때**: 상위 클래스(부모)가 흐름을 정의하되, 어떤 객체를 만들지는 하위 클래스(자식)에 맡기기 (Factory Method)
- **관련 객체를 세트로 생성해야 할 때**: 서로 관련된 여러 객체를 일관되게 생성 (Abstract Factory)

### 실제 사용 사례

- 피자 가게 (지역별로 다른 피자를 만드는 팩토리)
- 알림 시스템 (채널별로 다른 알림 객체 생성)
- DB 커넥션 (`create_engine("postgresql://...")` → 적절한 드라이버 반환)
- 파서 (파일 확장자에 따라 JSON/XML/CSV 파서 생성)

## 핵심 구조

### Simple Factory
가장 기본 형태. 생성 로직을 별도 함수/클래스로 분리.
- `create(type)` → 조건에 맞는 객체를 만들어 반환

### Factory Method
상위 클래스에서 객체 생성 메서드를 추상으로 선언하고, 하위 클래스가 구현.
- 상위 클래스: 흐름 정의 (`notify()` → `create_notification()` → `send()`)
- 하위 클래스: `create_notification()`을 오버라이드해서 어떤 객체를 만들지 결정

### Abstract Factory
관련 객체 군을 통째로 생성하는 인터페이스.
- `AbstractFactory.create_a()`, `create_b()` → 관련 객체들을 일관되게 생성

## Python 예제

→ `src/examples/factory_example.py`

## 주의할 점

- **Simple Factory로 충분하면 Factory Method까지 갈 필요 없음**: 생성 로직이 한 곳에서만 쓰이면 함수 하나면 충분
- **클래스 수 증가**: Factory Method는 제품 + Creator 클래스가 쌍으로 늘어남
- **Python에서는 함수로 대체 가능**: 딕셔너리 + 함수 조합이 클래스 기반보다 간결한 경우가 많음
