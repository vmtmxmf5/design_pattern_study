# Factory Pattern

## 한 줄 정의

객체 생성 로직을 별도의 메서드나 클래스로 분리하여, 클라이언트가 구체적인 클래스를 직접 지정하지 않고도 객체를 만들 수 있게 하는 패턴.

## 언제 사용하는가

- **생성할 객체의 종류가 조건에 따라 달라질 때**: if/else로 분기하며 `new`를 호출하는 코드가 여러 곳에 흩어져 있는 경우, 생성 로직을 한 곳으로 모을 수 있음
- **객체 생성 과정이 복잡하거나 변경될 가능성이 높을 때**: 생성 방식이 바뀌어도 클라이언트 코드는 수정할 필요 없음
- **프레임워크를 만들 때**: 상위 클래스에서 흐름을 정의하되, 어떤 객체를 만들지는 하위 클래스에 위임하고 싶은 경우 (Factory Method)
- **관련된 객체 군을 일관되게 생성해야 할 때**: 서로 관련된 여러 객체를 한 세트로 묶어 생성해야 하는 경우 (Abstract Factory)

### 실제 사용 사례

- 피자 가게 — Head First의 핵심 예제. `orderPizza("cheese")`에서 피자 종류마다 if/else로 `new`하던 코드를 Factory로 분리. 프랜차이즈(NY/Chicago) 확장 시 Factory Method로 발전: `PizzaStore.createPizza()`를 각 지역 서브클래스가 오버라이드
- DB 커넥션 생성 (`create_engine("postgresql://...")` → 적절한 드라이버 객체 반환)
- GUI 프레임워크 (OS에 따라 버튼, 스크롤바 등 위젯을 다르게 생성)
- 파서/시리얼라이저 (파일 확장자에 따라 JSON/XML/CSV 파서 생성)

## 핵심 구조

### Simple Factory

가장 기본 형태. 생성 로직을 별도 클래스로 분리한다. Head First에서는 "진짜 패턴은 아니지만 자주 쓰이는 관용구"라고 설명한다.

- `Factory.create(type)` → 조건에 맞는 구체 객체를 생성해서 반환
- 클라이언트는 Factory만 알면 되고, 구체 클래스를 직접 참조하지 않음

### Factory Method

상위 클래스에서 객체 생성 메서드를 추상으로 선언하고, 하위 클래스가 구현한다.

- 상위 클래스: 전체 흐름을 정의 (`order()` → `create()` → `process()`)
- 하위 클래스: `create()`를 오버라이드하여 어떤 객체를 만들지 결정
- 흐름은 고정하되, 생성되는 객체만 하위 클래스에서 교체

### Abstract Factory

관련된 객체 군을 통째로 생성하는 인터페이스를 제공한다.

- `AbstractFactory.create_a()`, `AbstractFactory.create_b()` → 서로 관련된 객체들을 일관되게 생성

## Python 예제

```python
from abc import ABC, abstractmethod


# --- Factory Method 예제: 알림 시스템 ---

class Notification(ABC):
    """알림 인터페이스"""

    @abstractmethod
    def send(self, message: str) -> None:
        pass


class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"[이메일] {message}")


class SlackNotification(Notification):
    def send(self, message: str) -> None:
        print(f"[슬랙] {message}")


class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f"[SMS] {message}")


class NotificationService(ABC):
    """Factory Method를 가진 상위 클래스"""

    @abstractmethod
    def create_notification(self) -> Notification:
        """하위 클래스가 어떤 알림 객체를 만들지 결정"""
        pass

    def notify(self, message: str) -> None:
        """흐름은 고정 — 생성만 하위 클래스에 위임"""
        notification = self.create_notification()
        notification.send(message)


class EmailService(NotificationService):
    def create_notification(self) -> Notification:
        return EmailNotification()


class SlackService(NotificationService):
    def create_notification(self) -> Notification:
        return SlackNotification()


class SMSService(NotificationService):
    def create_notification(self) -> Notification:
        return SMSNotification()


# 사용
services = [EmailService(), SlackService(), SMSService()]
for service in services:
    service.notify("서버 점검 예정")

# [이메일] 서버 점검 예정
# [슬랙] 서버 점검 예정
# [SMS] 서버 점검 예정


# --- Simple Factory: 간단한 버전 ---

def create_notification(channel: str) -> Notification:
    """조건에 따라 적절한 객체를 반환하는 팩토리 함수"""
    factories = {
        "email": EmailNotification,
        "slack": SlackNotification,
        "sms": SMSNotification,
    }
    if channel not in factories:
        raise ValueError(f"지원하지 않는 채널: {channel}")
    return factories[channel]()


notif = create_notification("slack")
notif.send("배포 완료")
# [슬랙] 배포 완료
```

## 주의할 점

- **Simple Factory로 충분하면 Factory Method까지 갈 필요 없음**: 생성 로직이 한 곳에서만 쓰이고 변경 가능성이 낮다면 단순 팩토리 함수면 충분
- **클래스 수 증가**: Factory Method는 제품 클래스 + Creator 클래스가 쌍으로 늘어남
- **Python에서는 함수로 대체 가능**: 클래스 기반 팩토리 대신 딕셔너리 + 함수 조합으로 간결하게 구현할 수 있음
