# Factory Pattern

## 한 줄 정의

객체를 만드는 코드를 별도로 분리하여, 클라이언트가 구체적인 클래스 이름을 몰라도 객체를 생성할 수 있게 하는 패턴.

## 언제 사용하는가

- **같은 종류의 객체 생성 코드가 여러 파일에 퍼져 있을 때**: `EmailNotification()`, `SlackNotification()` 같은 생성이 코드베이스 곳곳에 반복되면, 나중에 공통 변경(예: 생성 시 기본 설정을 추가해야 함)이 필요해졌을 때 한 군데라도 빠뜨리면 조용한 버그가 된다. 생성을 한 곳으로 모으면 고칠 곳도 한 곳.
- **새 타입이 앞으로 계속 늘어날 가능성이 높을 때**: 결제 수단, 파일 포맷, 알림 채널처럼 종류가 계속 추가되는 영역에서는, 팩토리를 쓰면 새 타입이 생겨도 기존 파일을 수정하지 않고 새 클래스 하나만 추가하면 된다 (Factory Method / Abstract Factory). 기존 코드를 안 건드린다는 건 기존 테스트가 깨질 위험이 없다는 뜻.

### 어느 변형을 선택할까

- **Simple Factory**: 조건에 따라 적절한 객체를 돌려주는 함수 하나면 충분할 때
- **Factory Method**: 부모 클래스에 여러 단계로 이뤄진 알고리즘이 있고, 그 중 "객체를 만드는 단계"를 자식 클래스가 오버라이드로 채우게 하고 싶을 때. Template Method 패턴과 거의 항상 짝을 이루어 쓰인다.
- **Abstract Factory**: 서로 관련된 여러 종류의 객체를 **한 세트로** 만들어야 하고, 다른 세트의 객체와 섞이면 안 될 때 (예: "Windows 버튼 + macOS 체크박스" 같은 조합이 생기면 안 되는 GUI 라이브러리)

### 실제 사용 사례

- 알림 시스템 (채널별로 다른 알림 객체 생성)
- DB 커넥션 (`create_engine("postgresql://...")` → 적절한 드라이버 반환)
- 파서 (파일 확장자에 따라 JSON/XML/CSV 파서 생성)
- 컴파일러 백엔드 (타겟 아키텍처별 코드 생성기 세트 — Abstract Factory)

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
