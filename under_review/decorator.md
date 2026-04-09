# Decorator Pattern

## 한 줄 정의

기존 객체를 감싸는 래퍼(감싸는 새 객체)를 통해, 원본 코드를 수정하지 않고 기능을 동적으로 추가하는 패턴. Python의 `@` 데코레이터 문법이 대표적인 예다.

## 언제 사용하는가

- **기존 코드를 수정하지 않고 기능을 추가해야 할 때**: 원본이 라이브러리에 있거나 변경이 위험한 경우
- **기능 조합이 다양할 때**: 상속으로 모든 조합을 만들면 클래스가 폭발적으로 늘어나는 경우
- **런타임에 기능을 붙이거나 떼야 할 때**: 실행 시점에 어떤 기능을 추가할지 결정해야 하는 경우

### 실제 사용 사례

- Python 데코레이터 (`@login_required`, `@cache`, `@timer`)
- Java I/O 스트림 (`BufferedInputStream`이 `FileInputStream`을 감쌈)
- 미들웨어 체인 (Django/Flask의 요청 처리 파이프라인)
- 음료 주문 시스템 (기본 음료 + 토핑 조합)

## 핵심 구조

**감싸기** — Decorator는 원본(Component)과 같은 인터페이스를 구현하면서, 내부에 Component를 가지고 있다. 원본 대신 사용할 수 있다.

**위임 + 추가 동작** — Decorator는 감싼 객체에게 원래 작업을 위임하고, 그 전후에 자신만의 동작을 추가한다.
- `Decorator(component)` → 원본 감쌈
- `Decorator.operation()` → 자신의 동작 + `component.operation()` 호출

여러 Decorator를 겹겹이 감쌀 수 있어서, 기능을 자유롭게 조합 가능.

## Python 예제

→ `src/examples/decorator_example.py`

## 주의할 점

- **구체 타입 의존 금지**: 클라이언트가 `isinstance`로 원본 타입을 확인하면 Decorator가 끼어들었을 때 깨짐
- **디버깅 어려움**: 래퍼가 겹겹이 쌓이면 호출 흐름 추적이 복잡해짐
- **Adapter와 혼동하지 말 것**: Decorator는 같은 인터페이스에 기능 추가, Adapter는 다른 인터페이스로 변환. 목적이 다름
