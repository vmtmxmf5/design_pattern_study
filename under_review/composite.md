# Composite Pattern

## 한 줄 정의

개별 객체와 복합 객체(그룹)를 동일한 인터페이스로 다루어, 트리 구조의 전체-부분 계층을 균일하게 처리하는 패턴.

## 언제 사용하는가

- **부분-전체 계층을 트리 구조로 표현해야 할 때**: 폴더 안에 파일과 하위 폴더가 있는 것처럼, 재귀적인 포함 관계를 표현해야 하는 경우
- **개별 객체와 그룹을 구분 없이 처리하고 싶을 때**: 클라이언트가 "이것이 단일 항목인지, 여러 항목의 묶음인지" 신경 쓰지 않고 동일한 메서드를 호출하고 싶은 경우
- **재귀적 구조에 일괄 연산을 적용해야 할 때**: 트리 전체에 대해 크기 합산, 출력, 검색 등의 연산을 한 번의 호출로 재귀적으로 수행하고 싶은 경우
- **새로운 종류의 항목을 추가해도 기존 코드를 변경하고 싶지 않을 때**: Component 인터페이스만 구현하면 단말 노드든 복합 노드든 자유롭게 추가할 수 있음

### 실제 사용 사례

- 메뉴 시스템 — Head First에서 Iterator 패턴에 이어 등장. 메뉴 안에 서브메뉴(디저트 메뉴 등)가 들어가야 하는데, 메뉴 항목(Leaf)과 서브메뉴(Composite) 모두를 동일한 인터페이스로 다루기 위해 Composite 도입
- 파일 시스템 (파일과 디렉터리의 재귀 구조)
- GUI 위젯 트리 (버튼은 단일 위젯, 패널은 위젯들의 컨테이너)
- 조직도 (직원과 부서의 계층 구조)

## 핵심 구조

**공통 인터페이스** — 단말 노드(Leaf)와 복합 노드(Composite) 모두 같은 Component 인터페이스를 구현한다. 클라이언트는 이 인터페이스만 사용하므로 둘을 구분할 필요가 없다.

**단말 노드 동작** — Leaf는 실제 작업을 수행하는 말단 객체이다.
- `Leaf.operation()` → 자기 자신의 작업을 직접 수행

**복합 노드 동작** — Composite는 자식 Component들을 관리하며, 요청을 자식들에게 재귀적으로 위임한다.
- `Composite.add(component)` → 자식 추가
- `Composite.remove(component)` → 자식 제거
- `Composite.operation()` → 모든 자식의 `operation()`을 재귀 호출하여 결과를 합산

## Python 예제

```python
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
        print(f"{'  ' * indent}📄 {self.name} ({self._size}KB)")


class Directory(FileSystemItem):
    """디렉터리 (Composite) — 파일과 하위 디렉터리를 포함할 수 있는 복합 노드"""

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
        print(f"{'  ' * indent}📁 {self.name} ({self.get_size()}KB)")
        for child in self._children:
            child.display(indent + 1)


# 사용
root = Directory("project")

src = Directory("src")
src.add(File("main.py", 15))
src.add(File("utils.py", 8))

tests = Directory("tests")
tests.add(File("test_main.py", 12))

root.add(src)
root.add(tests)
root.add(File("README.md", 3))

root.display()
# 📁 project (38KB)
#   📁 src (23KB)
#     📄 main.py (15KB)
#     📄 utils.py (8KB)
#   📁 tests (12KB)
#     📄 test_main.py (12KB)
#   📄 README.md (3KB)

print(f"\n전체 크기: {root.get_size()}KB")
# 전체 크기: 38KB

# 개별 파일이든 디렉터리든 동일한 메서드로 처리
items: list[FileSystemItem] = [src, File("config.json", 2)]
for item in items:
    print(f"{item.name}: {item.get_size()}KB")
# src: 23KB
# config.json: 2KB
```

## 주의할 점

- **Leaf에 불필요한 메서드**: Composite의 `add()`/`remove()`를 Component 인터페이스에 넣으면 Leaf에서도 이 메서드가 노출됨. 투명성과 안전성 사이에서 설계 판단이 필요함
- **타입 제한의 어려움**: Composite가 아무 Component나 받으므로, 특정 타입의 자식만 허용하고 싶을 때 별도 검증 로직이 필요함
- **양방향 참조**: 자식에서 부모로 거슬러 올라가야 한다면 부모 참조를 관리해야 하는데, 이때 메모리 관리에 주의해야 함
- **과도한 일반화**: 모든 구조를 Composite로 만들면 단순한 리스트로 충분한 상황에서도 불필요한 복잡성이 생김. 재귀적 트리 구조가 명확할 때만 적용할 것
