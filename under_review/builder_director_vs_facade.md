# Director vs Facade

둘 다 **여러 단계를 하나로 묶는다**는 점에서 비슷하지만, 목적이 다르다.

## 핵심 차이

| 구분 | Director (Builder의 일부) | Facade |
|------|--------------------------|--------|
| **목적** | 객체를 **생성**한다 | 작업을 **실행**한다 |
| **묶는 대상** | 빌더의 조립 단계들 | 서브시스템의 메서드들 |
| **결과물** | 완성된 객체 반환 | 작업 완료 (부수 효과) |
| **재사용** | 같은 조립 순서로 다른 객체를 만들 때 | 같은 작업 흐름을 반복 호출할 때 |

## 코드로 보는 차이

```python
# Director — 여러 조립 단계를 묶어서 "객체"를 만든다
def make_margherita(builder):
    builder.add_dough("thin")
    builder.add_sauce("tomato")
    builder.add_topping("mozzarella")
    return builder.build()  # ← 결과: Pizza 객체

# Facade — 여러 모듈을 묶어서 "작업"을 실행한다
class OrderFacade:
    def place_order(self, product, card, address):
        self._inventory.check(product)   # 재고 확인
        self._payment.charge(card)       # 결제
        self._shipping.ship(address)     # 배송
        # ← 결과: 주문이 처리됨 (객체 생성이 아님)
```

## 비유

```
Director = 레시피. 재료를 순서대로 조합해서 "완성된 요리"를 만든다.
Facade   = 컨시어지. 여러 부서에 연락해서 "일을 처리"해준다.
```

## 판단 기준

```
여러 단계를 하나로 묶는데...
├── 결과가 "객체"인가? → Director
│   (예: 피자 조립, SQL 쿼리 빌드, 비동기 파이프라인 구성)
│
└── 결과가 "작업 실행"인가? → Facade
    (예: 주문 처리, 영화 재생, 파일 업로드)
```
