"""Registry Pattern 예제: 직렬화 포맷 레지스트리

직렬화 포맷(JSON, CSV, YAML)을 이름으로 등록하고,
이름으로 찾아서 사용하는 예제.
새 포맷을 추가할 때 기존 코드를 수정할 필요가 없다.
"""

from abc import ABC, abstractmethod


class Serializer(ABC):
    """직렬화 인터페이스"""

    @abstractmethod
    def serialize(self, data: dict) -> str:
        pass


class JSONSerializer(Serializer):
    """JSON 형식으로 직렬화"""

    def serialize(self, data: dict) -> str:
        # 간단한 구현 (실제로는 json.dumps 사용)
        pairs = [f'"{k}": "{v}"' for k, v in data.items()]
        return "{" + ", ".join(pairs) + "}"


class CSVSerializer(Serializer):
    """CSV 형식으로 직렬화"""

    def serialize(self, data: dict) -> str:
        header = ",".join(data.keys())
        values = ",".join(str(v) for v in data.values())
        return f"{header}\n{values}"


class YAMLSerializer(Serializer):
    """YAML 형식으로 직렬화"""

    def serialize(self, data: dict) -> str:
        return "\n".join(f"{k}: {v}" for k, v in data.items())


class SerializerRegistry:
    """직렬화 포맷 레지스트리 — 이름으로 등록/조회"""

    def __init__(self) -> None:
        self._serializers: dict[str, Serializer] = {}

    def register(self, name: str, serializer: Serializer) -> None:
        """포맷 등록"""
        self._serializers[name] = serializer
        print(f"[등록] '{name}' 포맷 등록 완료")

    def get(self, name: str) -> Serializer:
        """이름으로 포맷 조회"""
        if name not in self._serializers:
            raise KeyError(f"등록되지 않은 포맷: '{name}'")
        return self._serializers[name]

    def list_formats(self) -> list[str]:
        """등록된 포맷 목록 반환"""
        return list(self._serializers.keys())


if __name__ == "__main__":
    # 레지스트리에 포맷 등록
    registry = SerializerRegistry()
    registry.register("json", JSONSerializer())
    registry.register("csv", CSVSerializer())
    registry.register("yaml", YAMLSerializer())

    print(f"\n등록된 포맷: {registry.list_formats()}")

    # 이름으로 찾아서 사용
    data = {"name": "김개발", "role": "backend", "level": "junior"}

    print("\n=== JSON ===")
    print(registry.get("json").serialize(data))

    print("\n=== CSV ===")
    print(registry.get("csv").serialize(data))

    print("\n=== YAML ===")
    print(registry.get("yaml").serialize(data))

    # 등록되지 않은 포맷 조회 시 에러
    try:
        registry.get("xml")
    except KeyError as e:
        print(f"\n[에러] {e}")
