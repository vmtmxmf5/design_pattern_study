"""Visitor Pattern 예제: 쇼핑몰 할인 계산

상품 클래스를 수정하지 않고, 새로운 연산(할인 계산, 세금 계산)을
Visitor 클래스로 추가하는 예제.
"""

from abc import ABC, abstractmethod

# --- Element: 방문 대상 ---


class Product(ABC):
    """상품 인터페이스 — accept()로 Visitor를 받아들인다"""

    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

    @abstractmethod
    def accept(self, visitor: "ProductVisitor") -> int:
        pass


class Book(Product):
    """도서 상품"""

    def accept(self, visitor: "ProductVisitor") -> int:
        return visitor.visit_book(self)


class Electronics(Product):
    """전자제품"""

    def accept(self, visitor: "ProductVisitor") -> int:
        return visitor.visit_electronics(self)


class Food(Product):
    """식품"""

    def accept(self, visitor: "ProductVisitor") -> int:
        return visitor.visit_food(self)


# --- Visitor: 새로운 연산 ---


class ProductVisitor(ABC):
    """상품 방문자 인터페이스"""

    @abstractmethod
    def visit_book(self, book: Book) -> int:
        pass

    @abstractmethod
    def visit_electronics(self, electronics: Electronics) -> int:
        pass

    @abstractmethod
    def visit_food(self, food: Food) -> int:
        pass


class DiscountVisitor(ProductVisitor):
    """할인 계산 Visitor — 상품 종류별로 다른 할인율 적용"""

    def visit_book(self, book: Book) -> int:
        discount = int(book.price * 0.1)  # 도서 10% 할인
        print(f"  [도서] {book.name}: {book.price}원 → {discount}원 할인")
        return discount

    def visit_electronics(self, electronics: Electronics) -> int:
        discount = int(electronics.price * 0.05)  # 전자제품 5% 할인
        print(
            f"  [전자] {electronics.name}: {electronics.price}원 → {discount}원 할인"
        )
        return discount

    def visit_food(self, food: Food) -> int:
        discount = 0  # 식품 할인 없음
        print(f"  [식품] {food.name}: {food.price}원 → 할인 없음")
        return discount


class TaxVisitor(ProductVisitor):
    """세금 계산 Visitor — 상품 종류별로 다른 세율 적용"""

    def visit_book(self, book: Book) -> int:
        tax = 0  # 도서 면세
        print(f"  [도서] {book.name}: 면세")
        return tax

    def visit_electronics(self, electronics: Electronics) -> int:
        tax = int(electronics.price * 0.1)  # 전자제품 10% 부가세
        print(f"  [전자] {electronics.name}: {tax}원 부가세")
        return tax

    def visit_food(self, food: Food) -> int:
        tax = 0  # 식품 면세
        print(f"  [식품] {food.name}: 면세")
        return tax


if __name__ == "__main__":
    # 상품 목록
    products: list[Product] = [
        Book("파이썬 입문", 25000),
        Electronics("키보드", 80000),
        Food("커피", 5000),
        Book("디자인 패턴", 35000),
    ]

    # 할인 계산 — 상품 클래스를 수정하지 않고 새 연산 적용
    print("=== 할인 계산 ===")
    discount_visitor = DiscountVisitor()
    total_discount = sum(p.accept(discount_visitor) for p in products)
    print(f"총 할인: {total_discount}원\n")

    # 세금 계산 — 또 다른 Visitor를 추가하기만 하면 됨
    print("=== 세금 계산 ===")
    tax_visitor = TaxVisitor()
    total_tax = sum(p.accept(tax_visitor) for p in products)
    print(f"총 세금: {total_tax}원")
