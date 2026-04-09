"""Command Pattern 예제: 스마트홈 리모컨

요청(행동)을 객체로 감싸서, 리모컨(Invoker)이 어떤 기기를 제어하는지 몰라도
execute()만 호출하면 되게 만드는 예제.
Undo 기능과 여러 명령을 묶는 매크로도 포함.
"""

from abc import ABC, abstractmethod

# --- Command 인터페이스 ---


class Command(ABC):
    """명령 인터페이스 — execute()와 undo()를 정의"""

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


# --- Receiver: 실제 동작을 수행하는 기기들 ---


class Light:
    """조명 — 켜기/끄기/밝기 조절이 가능한 기기"""

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
    """온도 조절기"""

    def __init__(self) -> None:
        self._temperature = 20

    def set_temperature(self, temp: int) -> None:
        self._temperature = temp
        print(f"온도 설정: {self._temperature}°C")

    @property
    def temperature(self) -> int:
        return self._temperature


# --- Concrete Command: 각 기기에 대한 구체적인 명령 ---


class LightOnCommand(Command):
    def __init__(self, light: Light):
        self._light = light
        self._prev_brightness = 0

    def execute(self) -> None:
        self._prev_brightness = self._light.brightness
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
        # 역순으로 되돌려야 올바르게 복원됨
        for cmd in reversed(self._commands):
            cmd.undo()


# --- Invoker: 명령을 실행하는 리모컨 ---


class RemoteControl:
    """리모컨 — 슬롯별로 명령을 할당하고 실행, Undo 지원"""

    def __init__(self, slots: int = 4):
        no_cmd: Command = NoCommand()
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


if __name__ == "__main__":
    # 기기 생성 (Receiver)
    living_light = Light("거실")
    bedroom_light = Light("침실")
    thermostat = Thermostat()

    # 리모컨에 명령 할당
    remote = RemoteControl()
    remote.set_command(0, LightOnCommand(living_light), LightOffCommand(living_light))
    remote.set_command(
        1, LightOnCommand(bedroom_light), LightOffCommand(bedroom_light)
    )
    remote.set_command(
        2,
        ThermostatSetCommand(thermostat, 25),
        ThermostatSetCommand(thermostat, 18),
    )

    # 리모컨은 execute()만 호출 — 어떤 기기인지 모름
    remote.press_on(0)
    # 거실 조명 켜짐 (밝기: 100%)

    remote.press_on(2)
    # 온도 설정: 25°C

    # Undo: 마지막 명령 되돌리기
    remote.press_undo()
    # 온도 설정: 20°C

    # 매크로: 외출 시 모든 조명 끄기 + 온도 낮추기
    go_out = MacroCommand(
        [
            LightOffCommand(living_light),
            LightOffCommand(bedroom_light),
            ThermostatSetCommand(thermostat, 15),
        ]
    )
    go_out.execute()
    # 거실 조명 꺼짐
    # 침실 조명 꺼짐
    # 온도 설정: 15°C

    go_out.undo()
    # 온도 설정: 20°C
    # 침실 조명 밝기: 0%
    # 거실 조명 밝기: 100%
