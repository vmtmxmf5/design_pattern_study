"""Flyweight Pattern 예제: 게임 나무 렌더링

대량의 나무 객체가 종류별 공유 데이터(이름, 색상, 텍스처)를 공유하고,
개별 데이터(x, y 좌표)만 따로 관리하여 메모리를 절약하는 예제.
"""


class TreeType:
    """나무 종류 (Flyweight) — 공유되는 고유 상태"""

    def __init__(self, name: str, color: str, texture: str):
        self.name = name
        self.color = color
        self.texture = texture

    def render(self, x: int, y: int) -> None:
        """공유 데이터 + 외부 좌표로 렌더링"""
        print(f"  [{self.name}] 색상={self.color}, 텍스처={self.texture} → 위치({x}, {y})")


class TreeFactory:
    """Flyweight Factory — 이미 만든 TreeType은 재사용"""

    _cache: dict[str, TreeType] = {}

    @classmethod
    def get_tree_type(cls, name: str, color: str, texture: str) -> TreeType:
        key = f"{name}_{color}_{texture}"
        if key not in cls._cache:
            print(f"  [팩토리] 새 TreeType 생성: {name}")
            cls._cache[key] = TreeType(name, color, texture)
        return cls._cache[key]

    @classmethod
    def cache_size(cls) -> int:
        return len(cls._cache)


class Tree:
    """개별 나무 — 외부 상태(좌표)만 가지고, 공유 데이터는 TreeType 참조"""

    def __init__(self, x: int, y: int, tree_type: TreeType):
        self._x = x
        self._y = y
        self._type = tree_type

    def render(self) -> None:
        self._type.render(self._x, self._y)


class Forest:
    """숲 — 대량의 나무를 관리"""

    def __init__(self) -> None:
        self._trees: list[Tree] = []

    def plant_tree(
        self, x: int, y: int, name: str, color: str, texture: str
    ) -> None:
        tree_type = TreeFactory.get_tree_type(name, color, texture)
        self._trees.append(Tree(x, y, tree_type))

    def render(self) -> None:
        for tree in self._trees:
            tree.render()


if __name__ == "__main__":
    forest = Forest()

    # 같은 종류의 나무를 여러 위치에 심기
    # TreeType은 종류당 하나만 생성됨
    forest.plant_tree(10, 20, "소나무", "초록", "pine.png")
    forest.plant_tree(30, 40, "소나무", "초록", "pine.png")  # 재사용
    forest.plant_tree(50, 60, "소나무", "초록", "pine.png")  # 재사용
    forest.plant_tree(15, 25, "단풍나무", "빨강", "maple.png")
    forest.plant_tree(35, 45, "단풍나무", "빨강", "maple.png")  # 재사용

    print(f"\n나무 {len(forest._trees)}그루, TreeType은 {TreeFactory.cache_size()}개만 생성")
    # 나무 5그루, TreeType은 2개만 생성

    print("\n=== 렌더링 ===")
    forest.render()
    # [소나무] 색상=초록, 텍스처=pine.png → 위치(10, 20)
    # [소나무] 색상=초록, 텍스처=pine.png → 위치(30, 40)
    # ...
