# Facade Pattern

## 한 줄 정의

여러 모듈의 실행을 묶는 메서드를 제공해, 호출자는 내부 과정을 몰라도 되게 하는 객체

```python
# 호출자는 이것만 호출하면 된다
order_facade.place_order(item)

# 내부에서는 여러 모듈이 순서대로 실행됨
# inventory.check() → payment.charge() → shipping.ship() → notification.send()
```

## 언제 사용하는가

- **내부 모듈의 세부 사항을 몰라도 쓸 수 있게 하고 싶을 때**: 호출자가 어떤 모듈을 어떤 순서로 호출해야 하는지 알 필요 없게
- **팀 간 협업에서 명확한 진입점을 제공해야 할 때**: "이 메서드만 호출하면 된다"는 인터페이스 제공

### 실제 사용 사례

- 주문 처리 시스템 (재고 확인 → 결제 → 배송 → 알림을 한 메서드로 묶음)
- 홈시어터 시스템 (프로젝터, 앰프, DVD, 조명을 `watchMovie()` 하나로 제어)
- ORM 라이브러리 (SQL, 커넥션, 트랜잭션을 하나의 API로 제공)
- 클라우드 SDK (인증, 네트워크, 직렬화를 숨기고 `client.upload()` 하나로 처리)

## 핵심 구조

**서브시스템(= 여러 모듈)** — 각자 독립적으로 동작하는 모듈들. `inventory`, `payment`, `shipping` 같은 것. Facade 없이도 직접 사용 가능.

**Facade** — 서브시스템의 모듈들을 알고 있고, 적절한 순서로 호출해서 작업을 완성한다. Facade가 내부 모듈을 다 알아야 하는 대신, 호출자는 몰라도 된다.

```python
class OrderFacade:
    def __init__(self):
        self._inventory = Inventory()
        self._payment = Payment()
        self._shipping = Shipping()
        self._notification = Notification()

    def place_order(self, product, card, address):
        self._inventory.check(product)       # 1단계
        self._payment.charge(card)           # 2단계
        self._shipping.ship(address)         # 3단계
        self._notification.send(email)       # 4단계
        # 호출자는 이 과정을 모른다!
```

Facade의 메서드는 하나가 아니라 여러 개일 수도 있다:

```python
class HomeTheaterFacade:
    def watch_movie(self):    # TV 켜기 + 스피커 켜기 + 조명 끄기
    def end_movie(self):      # TV 끄기 + 스피커 끄기 + 조명 켜기
    def listen_music(self):   # 스피커 켜기 + 조명 어둡게
```

## Python 예제

→ `src/examples/facade_example.py`

## 주의할 점

- **만능 객체가 되면 안 됨**: 서브시스템의 모든 기능을 Facade에 넣으면 거대한 God Object가 됨. 자주 쓰는 시나리오만 포함할 것
- **서브시스템 직접 접근 가능**: Facade는 편의를 제공하는 것이지, 직접 접근을 차단하는 게 아님. 세밀한 제어가 필요하면 모듈을 직접 호출해도 된다

```python
# Facade를 통해 (편하게)
order_facade.place_order(item)

# 직접 호출도 가능 (세밀한 제어가 필요하면)
inventory.check(item)
payment.charge(user, discount=0.1)  # 할인 적용 같은 세밀한 제어
```

- **Adapter와 혼동하지 말 것**: Adapter는 하나의 인터페이스를 변환, Facade는 여러 모듈을 하나로 묶어 단순화
