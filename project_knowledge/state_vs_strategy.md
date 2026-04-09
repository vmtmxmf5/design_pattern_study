# State vs Strategy: 언제 뭘 쓰는가

## 핵심 차이

**"행동 기준으로 묶을 것이냐, 상태 기준으로 묶을 것이냐"**

- **Strategy**: 행동(알고리즘) 기준으로 묶는다. 클라이언트가 직접 알고리즘을 선택한다.
- **State**: 상태 기준으로 묶는다. 상태 전환이 내부에서 자동으로 일어난다.

## 동전 뽑기 기계로 비교

### Strategy로 구현하면

행동 기준으로 코드가 나뉜다. `insert_quarter()`라는 행동 안에 모든 상태에 대한 분기가 들어간다.

```python
class GumballMachine:
    def insert_quarter(self):
        if self.state == "동전없음":
            print("동전 투입됨")
            self.state = "동전있음"
        elif self.state == "동전있음":
            print("이미 동전이 있습니다")
        elif self.state == "판매중":
            print("잠시 기다리세요")
        elif self.state == "품절":
            print("품절입니다")

    def turn_crank(self):
        if self.state == "동전없음":
            print("동전을 먼저 넣어주세요")
        elif self.state == "동전있음":
            print("손잡이 돌림!")
            self.state = "판매중"
        elif self.state == "판매중":
            print("이미 돌렸습니다")
        elif self.state == "품절":
            print("품절입니다")
```

**문제**: 상태가 하나 추가되면 (`"보너스"`) 모든 메서드의 if/else를 전부 수정해야 한다.

### State로 구현하면

상태 기준으로 코드가 나뉜다. "동전없음 상태에서 가능한 모든 행동"이 한 클래스에 모인다.

```python
class NoQuarterState:
    def insert_quarter(self, machine):
        print("동전 투입됨")
        machine.set_state(HasQuarterState())  # 상태 전환을 상태 클래스가 결정

    def turn_crank(self, machine):
        print("동전을 먼저 넣어주세요")

class HasQuarterState:
    def insert_quarter(self, machine):
        print("이미 동전이 있습니다")

    def turn_crank(self, machine):
        print("손잡이 돌림!")
        machine.set_state(SoldState())  # 다음 상태로 자동 전환
```

**장점**: 상태가 하나 추가되면 새 클래스 하나만 만들면 된다. 기존 코드 수정 없음.

### 그럼 Strategy는 언제 유리한가

뽑기 기계 같은 경우는 State가 맞지만, **결제 시스템**을 생각해보면 다르다.

```python
order = Order(CardPayment("1234-5678"))
order.checkout(50000)  # 카드 결제

order.set_strategy(PointPayment(10000))
order.checkout(3000)   # 포인트 결제로 교체
```

결제 수단은 "카드 → 포인트 → 계좌이체"로 자동 전환되지 않는다. **사용자가 직접 골라야 한다.** 또한 카드 결제가 포인트 결제의 존재를 알 필요도 없다. 이런 경우에는 Strategy가 유리하다.

만약 이걸 State로 구현하면, CardPayment가 다음 상태를 결정해야 하는데 — 결제 수단에는 "다음 상태"라는 개념 자체가 없으므로 어색해진다.

## 판단 기준

| | Strategy | State |
|---|---|---|
| **상태 전환** | 클라이언트가 직접 교체 | 내부에서 자동 발생 |
| **코드 묶음 단위** | 행동(알고리즘) 기준 | 상태 기준 |
| **객체 간 인식** | Strategy끼리 서로 모름 | State끼리 서로 알고 전환함 |
| **적합한 경우** | 결제 수단 선택처럼 클라이언트가 골라야 할 때 | 뽑기 기계처럼 상태가 자동으로 흘러갈 때 |
