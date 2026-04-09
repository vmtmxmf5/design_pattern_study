"""Event Bus Pattern 예제: 이벤트 기반 시스템

발행자와 구독자가 서로를 모른 채, 중앙 EventBus를 통해 이벤트를 주고받는 예제.
Observer 패턴과 달리 발행자가 구독자 목록을 직접 관리하지 않는다.
"""

from collections import defaultdict
from typing import Any, Callable


class EventBus:
    """중앙 이벤트 버스 — 이벤트 이름으로 발행/구독"""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable) -> None:
        """이벤트에 콜백 등록"""
        self._subscribers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable) -> None:
        """이벤트에서 콜백 제거"""
        self._subscribers[event_name].remove(callback)

    def publish(self, event_name: str, data: Any = None) -> None:
        """이벤트 발행 — 등록된 모든 콜백 호출"""
        for callback in self._subscribers[event_name]:
            callback(data)


# --- 구독자들 (서로의 존재를 모름) ---


def send_welcome_email(data: dict) -> None:
    """회원가입 시 환영 이메일 발송"""
    print(f"[이메일] {data['name']}님, 환영합니다!")


def grant_signup_coupon(data: dict) -> None:
    """회원가입 시 쿠폰 지급"""
    print(f"[쿠폰] {data['name']}님에게 가입 쿠폰 발급")


def log_event(data: Any) -> None:
    """모든 이벤트를 로깅"""
    print(f"[로그] 이벤트 수신: {data}")


def update_inventory(data: dict) -> None:
    """주문 시 재고 차감"""
    print(f"[재고] 상품 {data['product']} 재고 차감")


def notify_seller(data: dict) -> None:
    """주문 시 판매자에게 알림"""
    print(f"[알림] 판매자에게 주문 알림: {data['product']}")


if __name__ == "__main__":
    bus = EventBus()

    # 이벤트별 구독자 등록
    bus.subscribe("user_signup", send_welcome_email)
    bus.subscribe("user_signup", grant_signup_coupon)
    bus.subscribe("user_signup", log_event)

    bus.subscribe("order_placed", update_inventory)
    bus.subscribe("order_placed", notify_seller)
    bus.subscribe("order_placed", log_event)

    # 이벤트 발행 — 발행자는 구독자가 누구인지 모름
    print("=== 회원가입 이벤트 ===")
    bus.publish("user_signup", {"name": "김개발", "email": "dev@example.com"})
    # [이메일] 김개발님, 환영합니다!
    # [쿠폰] 김개발님에게 가입 쿠폰 발급
    # [로그] 이벤트 수신: {'name': '김개발', 'email': 'dev@example.com'}

    print("\n=== 주문 이벤트 ===")
    bus.publish("order_placed", {"product": "키보드", "quantity": 1})
    # [재고] 상품 키보드 재고 차감
    # [알림] 판매자에게 주문 알림: 키보드
    # [로그] 이벤트 수신: {'product': '키보드', 'quantity': 1}
