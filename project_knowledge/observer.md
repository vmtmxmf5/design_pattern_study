# Observer Pattern

## 한 줄 정의

감시 대상(Subject)의 상태가 변경되면, 이를 구독하고 있는 모든 감시자(Observer)에게 자동으로 알림을 보내는 패턴.

## 언제 사용하는가

- **이벤트 기반 시스템**: 특정 이벤트 발생 시 여러 컴포넌트가 반응해야 할 때
- **데이터 동기화**: 하나의 데이터 소스가 변경될 때 여러 뷰/화면이 동시에 갱신되어야 할 때 (예: MVC 패턴의 Model → View)
- **느슨한 결합이 필요할 때**: Subject는 Observer가 어떤 클래스인지 몰라도 됨. `update()` 메서드만 구현하면 어떤 객체든 Observer가 될 수 있음
- **런타임에 구독 관리가 필요할 때**: 실행 중에 Observer를 자유롭게 추가하거나 제거할 수 있어야 할 때
- **플러그인/확장 구조**: 새로운 Observer를 추가해도 Subject 코드를 수정할 필요 없음

### 실제 사용 사례

- GUI 이벤트 핸들링 (버튼 클릭 → 핸들러 호출)
- 주식/날씨 등 실시간 데이터 피드
- 메시지 브로커, Pub/Sub 시스템
- Django signals, React state 변경 감지

## 핵심 구조

**구독 관리** — Observer는 언제든 Subject에 등록/해제할 수 있다.
- `Subject.register(observer)` → 구독
- `Subject.remove(observer)` → 해제

**알림 흐름** — Subject의 상태가 변경되면 등록된 모든 Observer에게 알린다.
- `Subject.notify()` → 각 `Observer.update(data)` 호출

Subject 1개에 Observer N개가 연결되는 **one-to-many 관계**.

## Python 예제

→ `src/examples/observer_example.py`

## 주의할 점

- **순환 참조**: Subject와 Observer가 서로를 참조하면 GC 문제 발생 가능 → `weakref` 활용
- **알림 순서**: Observer 호출 순서에 의존하는 로직은 피할 것
- **과도한 알림**: 상태가 빈번히 변경되면 성능 문제 → 배치 업데이트나 debounce 고려
- **메모리 누수**: Observer 등록 후 해제하지 않으면 Subject가 계속 참조를 유지함
