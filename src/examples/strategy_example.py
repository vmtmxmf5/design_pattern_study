"""Strategy Pattern 예제: 결제 시스템"""

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """결제 전략 인터페이스"""

    @abstractmethod
    def pay(self, amount: int) -> None:
        pass


class CardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self._card_number = card_number

    def pay(self, amount: int) -> None:
        print(f"카드({self._card_number[-4:]}) {amount}원 결제")


class BankTransfer(PaymentStrategy):
    def __init__(self, account: str):
        self._account = account

    def pay(self, amount: int) -> None:
        print(f"계좌이체({self._account}) {amount}원 결제")


class PointPayment(PaymentStrategy):
    def __init__(self, points: int):
        self._points = points

    def pay(self, amount: int) -> None:
        if self._points >= amount:
            self._points -= amount
            print(f"포인트 {amount}P 사용 (잔여: {self._points}P)")
        else:
            print(f"포인트 부족 (보유: {self._points}P, 필요: {amount}P)")


class Order:
    """Context — 결제 전략을 위임받아 사용"""

    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy) -> None:
        """런타임에 결제 수단 변경"""
        self._strategy = strategy

    def checkout(self, amount: int) -> None:
        self._strategy.pay(amount)


if __name__ == "__main__":
    order = Order(CardPayment("1234-5678-9012-3456"))
    order.checkout(50000)
    # 카드(3456) 50000원 결제

    order.set_strategy(BankTransfer("110-123-456789"))
    order.checkout(30000)
    # 계좌이체(110-123-456789) 30000원 결제

    order.set_strategy(PointPayment(10000))
    order.checkout(8000)
    # 포인트 8000P 사용 (잔여: 2000P)
