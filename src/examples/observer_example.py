"""Observer Pattern 예제: 날씨 관측소"""

from abc import ABC, abstractmethod


class Observer(ABC):
    """옵저버 인터페이스"""

    @abstractmethod
    def update(self, data: dict) -> None:
        pass


class Subject:
    """Subject (Publisher) 기본 클래스"""

    def __init__(self):
        self._observers: list[Observer] = []

    def register(self, observer: Observer) -> None:
        self._observers.append(observer)

    def remove(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self.get_state())

    @abstractmethod
    def get_state(self) -> dict:
        pass


class WeatherStation(Subject):
    """날씨 데이터를 관리하는 Subject"""

    def __init__(self):
        super().__init__()
        self._temperature = 0.0
        self._humidity = 0.0

    def get_state(self) -> dict:
        return {"temperature": self._temperature, "humidity": self._humidity}

    def set_measurements(self, temp: float, humidity: float) -> None:
        self._temperature = temp
        self._humidity = humidity
        self.notify()  # 상태 변경 시 자동 알림


class CurrentConditionsDisplay(Observer):
    """현재 날씨를 표시하는 Observer"""

    def update(self, data: dict) -> None:
        print(f"현재 온도: {data['temperature']}°C, 습도: {data['humidity']}%")


class StatisticsDisplay(Observer):
    """통계를 표시하는 Observer"""

    def __init__(self):
        self._temps: list[float] = []

    def update(self, data: dict) -> None:
        self._temps.append(data["temperature"])
        avg = sum(self._temps) / len(self._temps)
        print(f"평균 온도: {avg:.1f}°C (측정 {len(self._temps)}회)")


if __name__ == "__main__":
    station = WeatherStation()

    current = CurrentConditionsDisplay()
    stats = StatisticsDisplay()

    station.register(current)
    station.register(stats)

    station.set_measurements(25.0, 65.0)
    # 현재 온도: 25.0°C, 습도: 65.0%
    # 평균 온도: 25.0°C (측정 1회)

    station.set_measurements(28.0, 70.0)
    # 현재 온도: 28.0°C, 습도: 70.0%
    # 평균 온도: 26.5°C (측정 2회)

    station.remove(current)  # 런타임에 구독 해제 가능

    station.set_measurements(22.0, 55.0)
    # 평균 온도: 25.0°C (측정 3회)  ← current는 더 이상 알림 안 받음
