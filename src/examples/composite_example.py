"""Composite Pattern 예제: 파일 시스템

파일(Leaf)과 디렉터리(Composite)를 동일한 인터페이스로 다루는 예제.
디렉터리 안에 파일과 하위 디렉터리가 들어갈 수 있고,
get_size()를 호출하면 재귀적으로 전체 크기를 합산한다.
"""

from abc import ABC, abstractmethod


class FileSystemItem(ABC):
    """파일 시스템 항목 인터페이스 (Component)"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> None:
        pass


class File(FileSystemItem):
    """파일 (Leaf) — 더 이상 하위 항목을 가질 수 없는 말단 노드"""

    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    def get_size(self) -> int:
        return self._size

    def display(self, indent: int = 0) -> None:
        print(f"{'  ' * indent}[파일] {self.name} ({self._size}KB)")


class Directory(FileSystemItem):
    """디렉터리 (Composite) — 파일과 하위 디렉터리를 포함하는 복합 노드"""

    def __init__(self, name: str):
        super().__init__(name)
        self._children: list[FileSystemItem] = []

    def add(self, item: FileSystemItem) -> None:
        self._children.append(item)

    def remove(self, item: FileSystemItem) -> None:
        self._children.remove(item)

    def get_size(self) -> int:
        """모든 자식의 크기를 재귀적으로 합산"""
        return sum(child.get_size() for child in self._children)

    def display(self, indent: int = 0) -> None:
        print(f"{'  ' * indent}[폴더] {self.name} ({self.get_size()}KB)")
        for child in self._children:
            child.display(indent + 1)


if __name__ == "__main__":
    # 트리 구조 생성
    root = Directory("project")

    src = Directory("src")
    src.add(File("main.py", 15))
    src.add(File("utils.py", 8))

    tests = Directory("tests")
    tests.add(File("test_main.py", 12))

    root.add(src)
    root.add(tests)
    root.add(File("README.md", 3))

    # 전체 트리 출력 — 재귀적으로 동작
    root.display()
    # [폴더] project (38KB)
    #   [폴더] src (23KB)
    #     [파일] main.py (15KB)
    #     [파일] utils.py (8KB)
    #   [폴더] tests (12KB)
    #     [파일] test_main.py (12KB)
    #   [파일] README.md (3KB)

    print(f"\n전체 크기: {root.get_size()}KB")
    # 전체 크기: 38KB

    # 개별 파일이든 디렉터리든 동일한 메서드로 처리
    items: list[FileSystemItem] = [src, File("config.json", 2)]
    for item in items:
        print(f"{item.name}: {item.get_size()}KB")
    # src: 23KB
    # config.json: 2KB
