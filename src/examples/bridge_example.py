"""Bridge Pattern 예제: 알림 시스템

알림 종류(긴급, 일반)와 전송 방식(이메일, SMS)을 독립적으로 확장할 수 있는 예제.
"무엇을 보낼지"(추상)와 "어떻게 보낼지"(구현)를 분리하여,
한쪽을 추가해도 다른 쪽을 수정할 필요가 없다.
"""

from abc import ABC, abstractmethod

# --- 구현 계층: "어떻게 보낼지" ---


class MessageSender(ABC):
    """메시지 전송 방식 인터페이스 (구현 계층)"""

    @abstractmethod
    def send(self, title: str, body: str) -> None:
        pass


class EmailSender(MessageSender):
    """이메일로 전송"""

    def send(self, title: str, body: str) -> None:
        print(f"[이메일] 제목: {title} | 내용: {body}")


class SMSSender(MessageSender):
    """SMS로 전송"""

    def send(self, title: str, body: str) -> None:
        print(f"[SMS] {title}: {body}")


class SlackSender(MessageSender):
    """Slack으로 전송"""

    def send(self, title: str, body: str) -> None:
        print(f"[Slack] *{title}* - {body}")


# --- 추상 계층: "무엇을 보낼지" ---


class Notification(ABC):
    """알림 인터페이스 (추상 계층) — 전송 방식을 주입받는다"""

    def __init__(self, sender: MessageSender):
        self._sender = sender

    @abstractmethod
    def notify(self, message: str) -> None:
        pass


class NormalNotification(Notification):
    """일반 알림 — 한 번 전송"""

    def notify(self, message: str) -> None:
        self._sender.send("알림", message)


class UrgentNotification(Notification):
    """긴급 알림 — [긴급] 표시를 붙여서 전송"""

    def notify(self, message: str) -> None:
        self._sender.send("[긴급] 알림", f"!!! {message} !!!")


if __name__ == "__main__":
    # 알림 종류 × 전송 방식을 자유롭게 조합
    normal_email = NormalNotification(EmailSender())
    normal_email.notify("회의가 10분 뒤 시작합니다")
    # [이메일] 제목: 알림 | 내용: 회의가 10분 뒤 시작합니다

    urgent_sms = UrgentNotification(SMSSender())
    urgent_sms.notify("서버 다운")
    # [SMS] [긴급] 알림: !!! 서버 다운 !!!

    urgent_slack = UrgentNotification(SlackSender())
    urgent_slack.notify("배포 실패")
    # [Slack] *[긴급] 알림* - !!! 배포 실패 !!!

    # 새로운 전송 방식(SlackSender)을 추가해도
    # 알림 종류(Normal, Urgent)는 수정할 필요 없다!
    normal_slack = NormalNotification(SlackSender())
    normal_slack.notify("코드 리뷰 요청이 있습니다")
    # [Slack] *알림* - 코드 리뷰 요청이 있습니다
