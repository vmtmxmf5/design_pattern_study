# Command Pattern

## 한 줄 정의

요청(행동)을 객체로 캡슐화하여, 요청의 발신자와 수신자를 분리하고, 요청을 저장하거나 취소하거나 큐에 넣을 수 있게 하는 패턴.

## 언제 사용하는가

- **요청을 나중에 실행해야 할 때**: 작업을 큐에 넣어두고 순서대로 처리하거나, 특정 시점에 실행해야 하는 경우
- **실행 취소(Undo)가 필요할 때**: 각 명령 객체가 실행 전 상태를 기억하고 있으므로, `undo()`를 호출해 이전 상태로 되돌릴 수 있음
- **요청을 로그로 남겨야 할 때**: 명령 객체를 직렬화하여 디스크에 저장하면, 시스템 장애 후 명령을 재실행하여 복구할 수 있음
- **발신자와 수신자를 분리해야 할 때**: 버튼이 어떤 동작을 실행하는지 몰라도 됨. 버튼은 `execute()`만 호출하면 되고, 실제 동작은 명령 객체가 결정함
- **매크로 명령이 필요할 때**: 여러 명령을 하나로 묶어서 한 번에 실행할 수 있음

### 실제 사용 사례

- 스마트홈 리모컨 — Head First의 핵심 예제. 7개 슬롯에 각각 on/off Command 객체를 할당. 리모컨(Invoker)은 `execute()`만 호출할 뿐, 어떤 기기가 어떤 동작을 하는지 모름
- GUI 버튼/메뉴 시스템 (각 버튼에 Command 객체를 할당)
- 텍스트 에디터의 Undo/Redo 스택
- 작업 큐와 스레드 풀 (명령 객체를 큐에 넣고 워커가 꺼내 실행)
- 트랜잭션 시스템 (명령을 로그로 저장하여 장애 복구에 활용)

Head First에서는 **식당 비유**로 패턴을 설명한다: 손님(Client)이 주문서(Command)를 작성 → 웨이트리스(Invoker)가 주문서를 전달 → 요리사(Receiver)가 실행. 웨이트리스는 주문 내용을 몰라도 `orderUp()`만 호출하면 된다.

## 핵심 구조

**명령 캡슐화** — 실행할 작업을 Command 객체로 감싼다. Command는 실제 작업을 수행하는 수신자(Receiver)를 내부에 가지고 있다.
- `Command(receiver)` → 수신자를 바인딩
- `Command.execute()` → `receiver.action()` 호출

**발신자와 수신자 분리** — 발신자(Invoker)는 Command 인터페이스만 알면 된다. 어떤 수신자가 어떤 작업을 하는지 전혀 모른다.
- `Invoker.set_command(command)` → 명령 할당
- `Invoker.press()` → `command.execute()` 호출

**실행 취소** — Command가 이전 상태를 저장하고, `undo()`로 되돌린다.
- `Command.execute()` → 실행 전 상태 저장 후 작업 수행
- `Command.undo()` → 저장된 상태로 복원

## Python 예제

```python
from abc import ABC, abstractmethod


class Command(ABC):
    """명령 인터페이스"""

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class NoCommand(Command):
    """아무 동작도 하지 않는 널 객체 — 슬롯 초기화용"""

    def execute(self) -> None:
        pass

    def undo(self) -> None:
        pass


# ── 수신자(Receiver) ──


class Light:
    """조명 — 실제 동작을 수행하는 수신자"""

    def __init__(self, location: str):
        self._location = location
        self._brightness = 0

    def on(self) -> None:
        self._brightness = 100
        print(f"{self._location} 조명 켜짐 (밝기: {self._brightness}%)")

    def off(self) -> None:
        self._brightness = 0
        print(f"{self._location} 조명 꺼짐")

    def dim(self, level: int) -> None:
        self._brightness = level
        print(f"{self._location} 조명 밝기: {self._brightness}%")

    @property
    def brightness(self) -> int:
        return self._brightness


class Thermostat:
    """온도 조절기 — 또 다른 수신자"""

    def __init__(self):
        self._temperature = 20

    def set_temperature(self, temp: int) -> None:
        self._temperature = temp
        print(f"온도 설정: {self._temperature}°C")

    @property
    def temperature(self) -> int:
        return self._temperature


# ── 구체 명령(Concrete Command) ──


class LightOnCommand(Command):
    def __init__(self, light: Light):
        self._light = light
        self._prev_brightness = 0

    def execute(self) -> None:
        self._prev_brightness = self._light.brightness  # 이전 상태 저장
        self._light.on()

    def undo(self) -> None:
        self._light.dim(self._prev_brightness)


class LightOffCommand(Command):
    def __init__(self, light: Light):
        self._light = light
        self._prev_brightness = 0

    def execute(self) -> None:
        self._prev_brightness = self._light.brightness
        self._light.off()

    def undo(self) -> None:
        self._light.dim(self._prev_brightness)


class ThermostatSetCommand(Command):
    def __init__(self, thermostat: Thermostat, temperature: int):
        self._thermostat = thermostat
        self._target_temp = temperature
        self._prev_temp = 0

    def execute(self) -> None:
        self._prev_temp = self._thermostat.temperature
        self._thermostat.set_temperature(self._target_temp)

    def undo(self) -> None:
        self._thermostat.set_temperature(self._prev_temp)


class MacroCommand(Command):
    """여러 명령을 하나로 묶는 매크로 명령"""

    def __init__(self, commands: list[Command]):
        self._commands = commands

    def execute(self) -> None:
        for cmd in self._commands:
            cmd.execute()

    def undo(self) -> None:
        for cmd in reversed(self._commands):
            cmd.undo()


# ── 발신자(Invoker) ──


class RemoteControl:
    """리모컨 — 슬롯별로 명령을 할당하고 실행"""

    def __init__(self, slots: int = 4):
        no_cmd = NoCommand()
        self._on_commands: list[Command] = [no_cmd] * slots
        self._off_commands: list[Command] = [no_cmd] * slots
        self._history: list[Command] = []

    def set_command(self, slot: int, on_cmd: Command, off_cmd: Command) -> None:
        self._on_commands[slot] = on_cmd
        self._off_commands[slot] = off_cmd

    def press_on(self, slot: int) -> None:
        cmd = self._on_commands[slot]
        cmd.execute()
        self._history.append(cmd)

    def press_off(self, slot: int) -> None:
        cmd = self._off_commands[slot]
        cmd.execute()
        self._history.append(cmd)

    def press_undo(self) -> None:
        if self._history:
            cmd = self._history.pop()
            cmd.undo()
        else:
            print("취소할 명령이 없습니다")


# 사용
living_light = Light("거실")
bedroom_light = Light("침실")
thermostat = Thermostat()

remote = RemoteControl()
remote.set_command(0, LightOnCommand(living_light), LightOffCommand(living_light))
remote.set_command(1, LightOnCommand(bedroom_light), LightOffCommand(bedroom_light))
remote.set_command(2, ThermostatSetCommand(thermostat, 25), ThermostatSetCommand(thermostat, 18))

remote.press_on(0)
# 거실 조명 켜짐 (밝기: 100%)

remote.press_on(2)
# 온도 설정: 25°C

remote.press_undo()
# 온도 설정: 20°C  ← undo로 이전 온도 복원

# 매크로: 외출 시 모든 조명 끄기 + 온도 낮추기
go_out = MacroCommand([
    LightOffCommand(living_light),
    LightOffCommand(bedroom_light),
    ThermostatSetCommand(thermostat, 15),
])
go_out.execute()
# 거실 조명 꺼짐
# 침실 조명 꺼짐
# 온도 설정: 15°C

go_out.undo()
# 온도 설정: 20°C
# 침실 조명 밝기: 0%
# 거실 조명 밝기: 100%  ← 역순으로 되돌림
```

## 주의할 점

- **Undo 상태 관리**: 복잡한 수신자의 경우 이전 상태를 정확히 저장하지 않으면 undo가 올바르게 동작하지 않음. 상태가 많으면 Memento 패턴과 함께 사용 고려
- **Command 클래스 수 증가**: 수신자와 동작 조합마다 Command 클래스가 필요함. 간단한 경우 Python에서는 람다나 `functools.partial`로 대체 가능
- **수신자 없는 Command**: 간단한 로직은 Command 자체에서 처리할 수도 있지만, 이렇게 하면 발신자-수신자 분리라는 패턴의 핵심 이점이 약해짐
- **매크로 명령의 부분 실패**: 매크로 실행 중 일부만 성공하면 undo 범위를 어디까지로 할지 결정해야 함
