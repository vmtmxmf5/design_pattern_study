# Facade Pattern

## 한 줄 정의

복잡한 서브시스템의 여러 인터페이스를 하나의 통합된 고수준 인터페이스로 묶어, 클라이언트가 쉽게 사용할 수 있게 하는 패턴.

## 언제 사용하는가

- **복잡한 서브시스템을 단순하게 사용하고 싶을 때**: 여러 클래스를 조합해야 하나의 작업이 완성되는 경우, 그 과정을 하나의 메서드로 묶고 싶을 때
- **서브시스템과 클라이언트 사이의 결합도를 낮추고 싶을 때**: 클라이언트가 서브시스템의 내부 구조를 몰라도 기능을 사용할 수 있게 하고 싶을 때
- **진입점을 명확히 제공해야 할 때**: 여러 팀이 협업하는 환경에서 "이 클래스만 호출하면 된다"는 명확한 인터페이스를 제공하고 싶을 때
- **레이어 사이의 경계를 만들 때**: 서비스 계층, 인프라 계층 등 아키텍처의 각 레이어에 깔끔한 진입점을 만들어야 할 때

### 실제 사용 사례

- 홈시어터 시스템 — Head First의 핵심 예제. 영화 한 편 보려면 프로젝터, 앰프, DVD 플레이어, 조명, 스크린, 팝콘 기계를 각각 조작해야 하는데, `HomeTheaterFacade.watchMovie()`로 한 번에 처리
- ORM 라이브러리 (SQL 문 조합, 커넥션 관리, 트랜잭션 처리를 하나의 API로 제공)
- 클라우드 SDK (인증, 네트워크, 직렬화를 숨기고 `client.upload(file)` 하나로 처리)
- 주문 처리 시스템 (재고 확인 → 결제 → 배송 접수를 하나로 묶음)

## 핵심 구조

**단순화된 진입점** — Facade는 서브시스템의 여러 클래스를 알고 있지만, 클라이언트는 Facade만 알면 된다.

**내부 위임** — Facade의 메서드는 서브시스템의 여러 객체를 적절한 순서로 호출하여 작업을 완성한다.

- `Client` → `Facade.do_something()` 호출
- `Facade.do_something()` 내부에서:
  - `SubsystemA.step1()` 호출
  - `SubsystemB.step2()` 호출
  - `SubsystemC.step3()` 호출

Facade는 서브시스템을 "감추는" 것이 아니라 "쉽게 쓸 수 있게" 해주는 것이다. 클라이언트가 원하면 서브시스템을 직접 호출할 수도 있다.

## Python 예제

```python
class InventoryService:
    """재고 관리 서브시스템"""

    def check_stock(self, product_id: str, quantity: int) -> bool:
        print(f"[재고] 상품 {product_id} 재고 확인: {quantity}개 요청")
        return True  # 재고 있음

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
        return "PAY-20260409-001"


class ShippingService:
    """배송 서브시스템"""

    def calculate_fee(self, address: str) -> int:
        print(f"[배송] 배송비 계산: {address}")
        return 3000

    def create_shipment(self, address: str, reservation_id: str) -> str:
        print(f"[배송] 배송 접수 완료 → {address}")
        return "SHIP-001"


class NotificationService:
    """알림 서브시스템"""

    def send_order_confirmation(self, email: str, order_id: str) -> None:
        print(f"[알림] {email}에 주문 확인 메일 발송 (주문번호: {order_id})")


class OrderFacade:
    """주문 퍼사드 — 복잡한 주문 과정을 하나의 메서드로 제공"""

    def __init__(self):
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


# 사용 — 클라이언트는 Facade만 알면 됨
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
# [배송] 배송 접수 완료 → 서울시 강남구 테헤란로 123
# [알림] user@example.com에 주문 확인 메일 발송 (주문번호: ORD-PAY-20260409-001-SHIP-001)

print(f"주문 완료: {order_id}")
```

## 주의할 점

- **Facade가 만능 객체가 되면 안 됨**: 서브시스템의 모든 기능을 Facade에 넣으면 거대한 클래스(God Object)가 됨. 자주 쓰는 시나리오만 포함할 것
- **서브시스템 직접 접근을 막지 않음**: Facade는 편의를 제공하는 것이지 서브시스템을 캡슐화하는 것이 아님. 세밀한 제어가 필요한 클라이언트는 서브시스템을 직접 사용할 수 있어야 함
- **Adapter와의 차이**: Adapter는 하나의 인터페이스를 다른 인터페이스로 변환하는 것이고, Facade는 여러 인터페이스를 하나로 묶어 단순화하는 것
- **최소 지식 원칙과 함께 사용**: Facade 패턴은 최소 지식 원칙(Law of Demeter)을 지키는 데 도움이 됨. 클라이언트가 알아야 하는 객체의 수를 줄여주기 때문
