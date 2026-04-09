# Adapter Pattern

## 한 줄 정의

기존 클래스의 인터페이스를 클라이언트가 기대하는 다른 인터페이스로 변환하여, 호환되지 않는 클래스들이 함께 동작할 수 있게 하는 패턴.

## 언제 사용하는가

- **기존 클래스를 수정할 수 없을 때**: 외부 라이브러리나 레거시 코드의 인터페이스가 현재 시스템과 맞지 않지만, 소스 코드를 변경할 권한이 없는 경우
- **서로 다른 인터페이스를 통합해야 할 때**: 두 시스템이 같은 기능을 제공하지만 메서드 이름이나 호출 방식이 다른 경우 (예: 외부 결제 API 교체 시 기존 코드 유지)
- **기존 코드를 재사용하고 싶을 때**: 잘 동작하는 기존 클래스를 새로운 설계에 맞춰 활용하고 싶지만, 인터페이스가 맞지 않는 경우
- **여러 외부 서비스를 하나의 인터페이스로 묶을 때**: 각기 다른 API를 가진 외부 서비스들을 동일한 방식으로 호출하고 싶은 경우

### 실제 사용 사례

- Turkey → Duck 변환 — Head First의 핵심 예제. Turkey는 `gobble()`과 짧은 `fly()`를 가지는데, Duck 인터페이스(`quack()`, `fly()`)에 맞추기 위해 TurkeyAdapter를 만든다. 현실의 AC 전원 어댑터와 동일한 개념
- 외부 API 통합 (결제사마다 다른 API를 하나의 인터페이스로 통일)
- 레거시 시스템 연동 (구형 시스템의 인터페이스를 신규 시스템에 맞게 변환)
- 데이터 포맷 변환 (XML 기반 시스템 → JSON 기반 시스템 연결)

## 핵심 구조

**변환 위임** — Adapter는 클라이언트가 기대하는 인터페이스(Target)를 구현하면서, 내부에 변환 대상(Adaptee)을 가지고 있다.

**호출 흐름** — 클라이언트는 Target 인터페이스를 호출하고, Adapter가 이를 Adaptee의 메서드로 변환하여 전달한다.

- `Client` → `Target.request()` 호출
- `Adapter.request()` → 내부에서 `Adaptee.specific_request()`로 변환하여 호출

클라이언트는 Adaptee의 존재를 모른다. Adapter가 중간에서 인터페이스 차이를 흡수한다.

## Python 예제

```python
from abc import ABC, abstractmethod


class NotificationSender(ABC):
    """알림 발송 인터페이스 — 우리 시스템이 기대하는 형태"""

    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass


class EmailService(NotificationSender):
    """기존 이메일 발송 서비스 — 이미 우리 인터페이스에 맞음"""

    def send(self, recipient: str, message: str) -> None:
        print(f"[이메일] {recipient}에게 발송: {message}")


class SlackAPI:
    """외부 Slack 라이브러리 — 우리 인터페이스와 다름"""

    def post_message(self, channel: str, text: str, icon: str = ":bell:") -> dict:
        print(f"[Slack] #{channel}에 전송: {text}")
        return {"ok": True, "channel": channel}


class KakaoAPI:
    """외부 카카오톡 라이브러리 — 역시 인터페이스가 다름"""

    def send_talk(self, phone_number: str, template_id: str, variables: dict) -> None:
        msg = variables.get("message", "")
        print(f"[카카오톡] {phone_number}에 발송: {msg}")


class SlackAdapter(NotificationSender):
    """Slack API를 NotificationSender 인터페이스에 맞게 변환"""

    def __init__(self, slack: SlackAPI):
        self._slack = slack

    def send(self, recipient: str, message: str) -> None:
        # recipient을 channel로, message를 text로 변환
        self._slack.post_message(channel=recipient, text=message)


class KakaoAdapter(NotificationSender):
    """카카오톡 API를 NotificationSender 인터페이스에 맞게 변환"""

    def __init__(self, kakao: KakaoAPI, template_id: str = "default"):
        self._kakao = kakao
        self._template_id = template_id

    def send(self, recipient: str, message: str) -> None:
        # recipient을 phone_number로, message를 variables로 변환
        self._kakao.send_talk(
            phone_number=recipient,
            template_id=self._template_id,
            variables={"message": message},
        )


def send_notification(sender: NotificationSender, recipient: str, message: str) -> None:
    """클라이언트 코드 — NotificationSender 인터페이스만 알면 됨"""
    sender.send(recipient, message)


# 사용
email = EmailService()
slack = SlackAdapter(SlackAPI())
kakao = KakaoAdapter(KakaoAPI(), template_id="order_complete")

# 동일한 인터페이스로 세 가지 채널에 발송
send_notification(email, "user@example.com", "주문이 완료되었습니다")
# [이메일] user@example.com에게 발송: 주문이 완료되었습니다

send_notification(slack, "order-alerts", "주문이 완료되었습니다")
# [Slack] #order-alerts에 전송: 주문이 완료되었습니다

send_notification(kakao, "010-1234-5678", "주문이 완료되었습니다")
# [카카오톡] 010-1234-5678에 발송: 주문이 완료되었습니다
```

## 주의할 점

- **Adapter가 너무 많은 변환을 하면 안 됨**: 단순 인터페이스 변환이 아니라 비즈니스 로직까지 넣으면 역할이 불분명해짐
- **양방향 Adapter는 복잡도를 높임**: 양쪽 인터페이스를 모두 구현하면 유지보수가 어려워지므로, 꼭 필요한 경우에만 사용할 것
- **Decorator와의 차이**: Decorator는 같은 인터페이스에 기능을 추가하는 것이고, Adapter는 다른 인터페이스로 변환하는 것. 목적이 다름
- **Facade와의 차이**: Facade는 복잡한 서브시스템을 단순화하는 것이고, Adapter는 호환되지 않는 인터페이스를 맞추는 것
