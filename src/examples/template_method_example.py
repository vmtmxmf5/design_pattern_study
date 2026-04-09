"""Template Method Pattern 예제: 데이터 파이프라인

데이터 처리 흐름(읽기 → 변환 → 저장)은 고정하고,
각 단계의 세부 구현만 하위 클래스에서 바꾸는 예제.
"""

from abc import ABC, abstractmethod


class DataPipeline(ABC):
    """데이터 파이프라인 뼈대 (Template Method)"""

    def run(self) -> None:
        """알고리즘 뼈대 — 이 순서는 고정, 하위 클래스가 바꿀 수 없다"""
        data = self.read()
        transformed = self.transform(data)
        if self.should_validate():  # 훅(Hook): 필요할 때만 오버라이드
            self.validate(transformed)
        self.save(transformed)
        print(f"[완료] {self.__class__.__name__} 파이프라인 종료\n")

    @abstractmethod
    def read(self) -> list[dict]:
        """데이터 읽기 — 하위 클래스가 반드시 구현"""
        pass

    @abstractmethod
    def transform(self, data: list[dict]) -> list[dict]:
        """데이터 변환 — 하위 클래스가 반드시 구현"""
        pass

    @abstractmethod
    def save(self, data: list[dict]) -> None:
        """데이터 저장 — 하위 클래스가 반드시 구현"""
        pass

    def should_validate(self) -> bool:
        """훅(Hook) — 기본은 False, 필요하면 오버라이드"""
        return False

    def validate(self, data: list[dict]) -> None:
        """검증 단계 — 훅이 True일 때만 실행"""
        print(f"[검증] {len(data)}건 데이터 검증 통과")


class CSVPipeline(DataPipeline):
    """CSV 데이터 파이프라인"""

    def read(self) -> list[dict]:
        print("[읽기] CSV 파일에서 데이터 로드")
        return [{"name": "Alice", "score": "85"}, {"name": "Bob", "score": "92"}]

    def transform(self, data: list[dict]) -> list[dict]:
        print("[변환] score를 문자열 → 정수로 변환")
        return [{**row, "score": int(row["score"])} for row in data]

    def save(self, data: list[dict]) -> None:
        for row in data:
            print(f"[저장] {row}")


class APIPipeline(DataPipeline):
    """API 데이터 파이프라인 — 검증 단계 포함"""

    def read(self) -> list[dict]:
        print("[읽기] API에서 데이터 수신")
        return [{"user": "Charlie", "active": True}, {"user": "Dave", "active": False}]

    def transform(self, data: list[dict]) -> list[dict]:
        print("[변환] 활성 사용자만 필터링")
        return [row for row in data if row["active"]]

    def save(self, data: list[dict]) -> None:
        for row in data:
            print(f"[저장] {row}")

    def should_validate(self) -> bool:
        """API 데이터는 검증 필요 — 훅 오버라이드"""
        return True


if __name__ == "__main__":
    print("=== CSV 파이프라인 ===")
    CSVPipeline().run()
    # [읽기] CSV 파일에서 데이터 로드
    # [변환] score를 문자열 → 정수로 변환
    # [저장] {'name': 'Alice', 'score': 85}
    # [저장] {'name': 'Bob', 'score': 92}
    # [완료] CSVPipeline 파이프라인 종료

    print("=== API 파이프라인 ===")
    APIPipeline().run()
    # [읽기] API에서 데이터 수신
    # [변환] 활성 사용자만 필터링
    # [검증] 1건 데이터 검증 통과     ← 훅이 True이므로 검증 실행
    # [저장] {'user': 'Charlie', 'active': True}
    # [완료] APIPipeline 파이프라인 종료
