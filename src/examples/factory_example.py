"""Factory Pattern 예제: 알림 시스템

객체 생성 로직을 별도로 분리하여,
클라이언트가 구체 클래스를 직접 지정하지 않고도 객체를 만드는 예제.
Factory Method와 Simple Factory 두 가지 방식을 모두 보여준다.
"""

from abc import ABC, abstractmethod

# --- Product: 생성될 객체들 ---


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


# --- Factory Method: 상위 클래스가 흐름을 정의, 하위 클래스가 생성을 결정 ---


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


# --- Simple Factory: 조건에 따라 적절한 객체를 반환하는 함수 ---


def create_notification(channel: str) -> Notification:
    """팩토리 함수 — 채널 이름에 맞는 알림 객체를 생성"""
    factories: dict[str, type[Notification]] = {
        "email": EmailNotification,
        "slack": SlackNotification,
        "sms": SMSNotification,
    }
    if channel not in factories:
        raise ValueError(f"지원하지 않는 채널: {channel}")
    return factories[channel]()


if __name__ == "__main__":
    # Factory Method 방식: 서비스마다 다른 알림 객체를 생성
    print("=== Factory Method ===")
    services: list[NotificationService] = [
        EmailService(),
        SlackService(),
        SMSService(),
    ]
    for service in services:
        service.notify("서버 점검 예정")
    # [이메일] 서버 점검 예정
    # [슬랙] 서버 점검 예정
    # [SMS] 서버 점검 예정

    # Simple Factory 방식: 문자열로 객체 생성
    print("\n=== Simple Factory ===")
    notif = create_notification("slack")
    notif.send("배포 완료")
    # [슬랙] 배포 완료
