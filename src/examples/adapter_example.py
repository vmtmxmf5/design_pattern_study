"""Adapter Pattern 예제: 알림 발송 시스템

서로 다른 외부 API(Slack, 카카오톡)를 하나의 인터페이스로 통일하는 예제.
각 API의 메서드 이름과 호출 방식이 다르지만,
Adapter를 통해 동일한 send() 메서드로 사용할 수 있다.
"""

from abc import ABC, abstractmethod

# --- Target: 우리 시스템이 기대하는 인터페이스 ---

class NotificationSender(ABC):
    """알림 발송 인터페이스 (Target)"""

    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass


# --- 이미 인터페이스에 맞는 클래스 ---

class EmailService(NotificationSender):
    """이메일 발송 — 이미 우리 인터페이스(send)에 맞음"""

    def send(self, recipient: str, message: str) -> None:
        print(f"[이메일] {recipient}에게 발송: {message}")


# --- Adaptee: 인터페이스가 다른 외부 API들 ---

class SlackAPI:
    """외부 Slack API — post_message()를 사용, 우리 인터페이스와 다름"""

    def post_message(self, channel: str, text: str) -> dict:
        print(f"[Slack] #{channel}에 전송: {text}")
        return {"ok": True, "channel": channel}


class KakaoAPI:
    """외부 카카오톡 API — send_talk()을 사용, 역시 인터페이스가 다름"""

    def send_talk(self, phone_number: str, template_id: str, variables: dict) -> None:
        msg = variables.get("message", "")
        print(f"[카카오톡] {phone_number}에 발송: {msg}")


# --- Adapter: 외부 API를 우리 인터페이스에 맞게 변환 ---

class SlackAdapter(NotificationSender):
    """Slack API를 NotificationSender 인터페이스에 맞게 감싸는 어댑터"""

    def __init__(self, slack: SlackAPI):
        self._slack = slack

    def send(self, recipient: str, message: str) -> None:
        # recipient → channel, message → text로 변환
        self._slack.post_message(channel=recipient, text=message)


class KakaoAdapter(NotificationSender):
    """카카오톡 API를 NotificationSender 인터페이스에 맞게 감싸는 어댑터"""

    def __init__(self, kakao: KakaoAPI, template_id: str = "default"):
        self._kakao = kakao
        self._template_id = template_id

    def send(self, recipient: str, message: str) -> None:
        # recipient → phone_number, message → variables로 변환
        self._kakao.send_talk(
            phone_number=recipient,
            template_id=self._template_id,
            variables={"message": message},
        )


# --- 클라이언트 코드 ---

def send_notification(sender: NotificationSender, recipient: str, message: str) -> None:
    """NotificationSender 인터페이스만 알면 됨 — 어떤 채널이든 동일하게 호출"""
    sender.send(recipient, message)


if __name__ == "__main__":
    email = EmailService()
    slack = SlackAdapter(SlackAPI())
    kakao = KakaoAdapter(KakaoAPI(), template_id="order_complete")

    # 세 가지 채널 모두 동일한 방식으로 호출
    send_notification(email, "user@example.com", "주문이 완료되었습니다")
    # [이메일] user@example.com에게 발송: 주문이 완료되었습니다

    send_notification(slack, "order-alerts", "주문이 완료되었습니다")
    # [Slack] #order-alerts에 전송: 주문이 완료되었습니다

    send_notification(kakao, "010-1234-5678", "주문이 완료되었습니다")
    # [카카오톡] 010-1234-5678에 발송: 주문이 완료되었습니다
