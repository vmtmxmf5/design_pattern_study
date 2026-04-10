# Facade vs Registry

둘 다 **"하나의 진입점"**을 제공하지만, 제공하는 것이 다르다.

## 핵심 차이

| 구분 | Facade | Registry |
|------|--------|----------|
| **제공하는 것** | 간단한 메서드 (복잡한 과정을 숨김) | 객체 조회 (이름으로 찾기) |
| **내부 로직** | 서브시스템을 적절한 순서로 조율 | 딕셔너리에서 꺼내줌 (로직 없음) |
| **클라이언트가 아는 것** | "이 메서드 하나만 호출하면 끝" | "이름을 알면 객체를 찾을 수 있다" |
| **확장 방식** | Facade에 메서드 추가 | Registry에 객체 등록 |

## 프론트 데스크로 비유하면

```
Facade   = 호텔 컨시어지. "레스토랑 예약해주세요" 하면 알아서 검색, 전화, 확인까지 다 해줌.
           복잡한 과정을 하나의 요청으로 처리해주는 것이 핵심

Registry = 호텔 내선번호표. "프론트: 0번, 룸서비스: 1번, 수영장: 2번"
           이름(번호)으로 원하는 서비스를 찾아서 직접 연락하는 것
```

## 판단 기준

```
클라이언트가 원하는 게 뭔가?
├── "복잡한 건 알아서 해줘, 결과만 줘" → Facade
│   (예: OrderFacade.place_order() → 재고+결제+배송+알림 한 번에)
│
└── "내가 직접 쓸 건데, 이름으로 찾게 해줘" → Registry
    (예: registry.get("json") → JSONSerializer 객체 반환, 직접 사용)
```

## 코드로 보는 차이

```python
# Facade: 복잡한 과정을 하나로 묶어서 처리
class OrderFacade:
    def place_order(self, product, card, address):
        self._inventory.check(product)    # 1단계
        self._payment.charge(card)        # 2단계
        self._shipping.ship(address)      # 3단계
        self._notification.send(email)    # 4단계
        # 클라이언트는 이 과정을 모름!

# Registry: 이름으로 객체를 찾아서 돌려줌
class SerializerRegistry:
    def get(self, name: str) -> Serializer:
        return self._serializers[name]
        # 클라이언트가 직접 사용: registry.get("json").serialize(data)
```

## 함께 쓰는 경우

Facade 내부에서 Registry를 사용하는 조합도 가능하다. 예: `OrderFacade`가 결제 수단을 Registry에서 찾아서 사용.
