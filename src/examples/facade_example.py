"""Facade Pattern 예제: 주문 처리 시스템

재고 확인 → 결제 → 배송 → 알림이라는 복잡한 과정을
OrderFacade.place_order() 하나로 묶어서 제공하는 예제.
클라이언트는 서브시스템의 세부 사항을 몰라도 된다.
"""


class InventoryService:
    """재고 관리 서브시스템"""

    def check_stock(self, product_id: str, quantity: int) -> bool:
        print(f"[재고] 상품 {product_id} 재고 확인: {quantity}개 요청")
        return True

    def reserve(self, product_id: str, quantity: int) -> str:
        print(f"[재고] 상품 {product_id} {quantity}개 예약 완료")
        return f"RSV-{product_id}-001"


class PaymentService:
    """결제 서브시스템"""

    def validate_card(self, card_number: str) -> bool:
        print(f"[결제] 카드 유효성 검증: ****{card_number[-4:]}")
        return True

    def charge(self, card_number: str, amount: int) -> str:
        print(f"[결제] {amount}원 결제 완료")
        return "PAY-001"


class ShippingService:
    """배송 서브시스템"""

    def calculate_fee(self, address: str) -> int:
        print(f"[배송] 배송비 계산: {address}")
        return 3000

    def create_shipment(self, address: str, reservation_id: str) -> str:
        print(f"[배송] 배송 접수 완료 -> {address}")
        return "SHIP-001"


class NotificationService:
    """알림 서브시스템"""

    def send_order_confirmation(self, email: str, order_id: str) -> None:
        print(f"[알림] {email}에 주문 확인 메일 발송 (주문번호: {order_id})")


class OrderFacade:
    """주문 퍼사드 — 복잡한 주문 과정을 하나의 메서드로 제공"""

    def __init__(self) -> None:
        self._inventory = InventoryService()
        self._payment = PaymentService()
        self._shipping = ShippingService()
        self._notification = NotificationService()

    def place_order(
        self,
        product_id: str,
        quantity: int,
        card_number: str,
        address: str,
        email: str,
    ) -> str:
        """주문 전체 과정을 한 번에 처리"""
        # 1. 재고 확인 및 예약
        if not self._inventory.check_stock(product_id, quantity):
            raise ValueError("재고가 부족합니다")
        reservation_id = self._inventory.reserve(product_id, quantity)

        # 2. 결제
        if not self._payment.validate_card(card_number):
            raise ValueError("유효하지 않은 카드입니다")
        shipping_fee = self._shipping.calculate_fee(address)
        unit_price = 29000
        total = unit_price * quantity + shipping_fee
        payment_id = self._payment.charge(card_number, total)

        # 3. 배송 접수
        shipment_id = self._shipping.create_shipment(address, reservation_id)

        # 4. 주문 확인 알림
        order_id = f"ORD-{payment_id}-{shipment_id}"
        self._notification.send_order_confirmation(email, order_id)

        return order_id


if __name__ == "__main__":
    # 클라이언트는 Facade만 알면 됨
    facade = OrderFacade()

    order_id = facade.place_order(
        product_id="ITEM-42",
        quantity=2,
        card_number="1234-5678-9012-3456",
        address="서울시 강남구 테헤란로 123",
        email="user@example.com",
    )
    # [재고] 상품 ITEM-42 재고 확인: 2개 요청
    # [재고] 상품 ITEM-42 2개 예약 완료
    # [결제] 카드 유효성 검증: ****3456
    # [배송] 배송비 계산: 서울시 강남구 테헤란로 123
    # [결제] 61000원 결제 완료
    # [배송] 배송 접수 완료 -> 서울시 강남구 테헤란로 123
    # [알림] user@example.com에 주문 확인 메일 발송 (주문번호: ORD-PAY-001-SHIP-001)

    print(f"\n주문 완료: {order_id}")
