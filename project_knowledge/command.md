# Command Pattern

## 한 줄 정의

함수 호출을 객체로 만드는 패턴

## 언제 사용하는가

- **호출자와 실제 동작의 분리** — 새 동작이 추가되어도 호출자(invoker) 코드를 수정할 필요가 없다
- **작업 되돌리기 기능 필요** — 함수 호출은 이전 상태를 기억할 수 없지만, 객체는 저장해둘 수 있기 때문에 복원이 가능
- **관련된 명령을 연쇄적으로 실행/취소하고 싶을 때** — 예: 영화 예매, 식당 예약, 택시 호출을 하나로 묶어 한 번에 실행/취소
- **실행 시점 선택** — 큐에 넣어서 순서대로 처리하거나, 실행 시점을 나중으로 미룰 수 있다

## 핵심 구조

**Command** — 함수 호출을 감싸는 객체. 내부에 `execute()`와 `undo()`를 가진다. 또한, 실제 작업 대상인 Receiver를 가지고 있다.
- 예: `TurnOffLight(light)` — `light`(Receiver)에게 꺼지라고 시키는 객체

**Invoker** — Command의 `execute()`를 호출하는 주체(=호출자). 안에 뭐가 들어있는지 모르고, 그냥 실행만 한다.
- 흐름: Invoker → Command → Receiver. 
- 예: 리모컨(Invoker)이 `TurnOffLight`(Command)를 받고, `TurnOffLight`(Command)가 `light`(Receiver)를 받는다

**Receiver** — Command가 실제로 일을 시키는 대상. 조명, 에어컨 같은 기기.

**Undo** — Command가 실행 전 상태를 저장해두고, `undo()`로 복원한다.

## Python 예제

→ `src/examples/command_example.py`

## 주의할 점

- **Undo 상태 관리**: Receiver의 상태가 복잡할수록 이전 상태를 정확히 저장하기 어려움. 상태가 많으면 Memento 패턴과 함께 사용 고려
- **Command 클래스 수 증가**: 동작마다 클래스가 필요함. 간단한 경우 Python에서는 람다나 `functools.partial`로 대체 가능
- **매크로의 부분 실패**: 영화 예매 성공, 식당 예약 성공, 택시 호출 실패 — 이때 전부 undo할지, 실패한 것만 빼고 유지할지 결정이 필요함
