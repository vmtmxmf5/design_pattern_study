"""Singleton Pattern 예제: 설정 관리자

앱 전체에서 설정 객체가 하나만 존재하도록 보장하는 예제.
어디서 접근하든 같은 인스턴스를 반환한다.
"""


class AppConfig:
    """앱 설정 — 인스턴스가 하나만 존재하도록 보장"""

    _instance: "AppConfig | None" = None

    def __new__(cls) -> "AppConfig":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # 최초 생성 시에만 초기화
            cls._instance._settings: dict[str, str] = {}
            cls._instance._initialized = False
        return cls._instance

    def initialize(self, **settings: str) -> None:
        """설정 초기화 (최초 1회)"""
        if not self._initialized:
            self._settings.update(settings)
            self._initialized = True
            print(f"[설정] 초기화 완료: {self._settings}")
        else:
            print("[설정] 이미 초기화되었습니다")

    def get(self, key: str, default: str = "") -> str:
        """설정값 조회"""
        return self._settings.get(key, default)

    def set(self, key: str, value: str) -> None:
        """설정값 변경"""
        self._settings[key] = value
        print(f"[설정] {key} = {value}")

    def show_all(self) -> None:
        """전체 설정 출력"""
        for key, value in self._settings.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    # 어디서 생성하든 같은 인스턴스
    config1 = AppConfig()
    config2 = AppConfig()

    print(f"같은 인스턴스인가? {config1 is config2}")
    # 같은 인스턴스인가? True

    # 초기화
    config1.initialize(db_host="localhost", db_port="5432", debug="true")
    # [설정] 초기화 완료: {'db_host': 'localhost', 'db_port': '5432', 'debug': 'true'}

    # 이미 초기화되었으므로 무시
    config2.initialize(db_host="remote-server")
    # [설정] 이미 초기화되었습니다

    # config2에서 변경하면 config1에서도 반영됨 (같은 인스턴스)
    config2.set("debug", "false")
    # [설정] debug = false

    print(f"\nconfig1에서 조회: debug = {config1.get('debug')}")
    # config1에서 조회: debug = false

    print("\n전체 설정:")
    config1.show_all()
