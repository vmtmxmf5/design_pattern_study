# Composite Pattern

## 한 줄 정의

폴더와 파일처럼 "묶음"과 "단일 항목"이 섞인 트리 구조를, 호출자가 둘을 구분하지 않고 한 번의 호출로 처리할 수 있게 하는 패턴.

### 한 눈에 보기

폴더 안에 파일과 하위 폴더가 섞여 있을 때, 총 용량을 어떻게 구할까?

```
project/
├── src/
│   ├── main.py        (15 KB)
│   └── utils.py       (8 KB)
├── tests/
│   └── test_main.py   (12 KB)
└── README.md          (3 KB)
```

`project/`의 총 용량은 38 KB. 이걸 코드로는 어떻게 구하나?

```python
# Before — 호출자가 타입 체크를 떠안음
def total_size(node):
    if isinstance(node, File):
        return node.bytes
    elif isinstance(node, Folder):
        return sum(total_size(c) for c in node.children)
```

새 종류(압축파일, 클라우드 폴더…)가 생길 때마다 이 함수에 `elif`가 추가된다.

```python
# After — Composite 적용
class File:
    def __init__(self, bytes):
        self.bytes = bytes
    def get_size(self):
        return self.bytes

class Folder:
    def __init__(self, children):
        self.children = children
    def get_size(self):
        return sum(c.get_size() for c in self.children)

# 위 트리를 코드로 (이름은 생략, 크기만)
root = Folder([
    Folder([File(15), File(8)]),    # src/
    Folder([File(12)]),              # tests/
    File(3),                         # README.md
])

total = root.get_size()   # → 38. 분기 없음.
```

호출자는 루트가 파일인지 폴더인지 모른다. 그냥 `.get_size()`만 부르면 — 폴더는 자식들에게 같은 메서드를 다시 묻고, 그 자식이 또 폴더면 또 묻고… **트리 전체가 자동으로 풀린다**.

## 언제 사용하는가

- **트리 구조에 같은 연산을 일괄 적용해야 할 때**: 폴더 용량 합산, 메뉴 트리 렌더링, GUI 위젯 갱신처럼 모든 노드에 같은 동작을 적용해야 하는 상황. 호출자는 루트에 한 번만 호출하면 트리 전체가 자동으로 처리된다.
- **호출자가 노드 타입을 매번 체크하는 게 싫을 때**: 위 Before 코드 같은 `isinstance` 분기가 호출부마다 반복되는 걸 막고 싶을 때. Composite는 그 분기를 객체 자체에 숨겨버린다.
- **앞으로 새 노드 종류가 추가될 가능성이 있을 때**: 압축파일, 클라우드 폴더, 심볼릭 링크처럼 새 종류가 생겨도 호출자 코드는 그대로 두고 새 클래스만 추가하면 된다.

### 적용 범위 — "트리"에 한정

Composite는 부분-전체(part-whole) 관계의 트리 구조에서만 작동한다. 사이클이 있는 그래프나 평탄한 리스트엔 적합하지 않다 (재귀가 무한 루프에 빠지거나, 재귀할 게 없음).

다만 "트리"의 범위가 생각보다 넓다 — "X가 Y를 품고, Y가 다시 X와 같은 종류일 수 있다"는 구조면 다 트리다.

### 실제 사용 사례

- 파일 시스템 (폴더 ↔ 파일)
- HTML DOM (`<div>` 안에 `<p>`, `<span>` 등)
- 컴파일러 AST / 수식 표현 트리 (`(a+b)*(c-d)`에서 `*`가 `+`와 `-`를 자식으로)
- GUI 위젯 트리 (Window → Panel → Button)
- JSON 데이터 (object/array가 또 object/array를 품음)
- 조직도 (회사 → 본부 → 팀 → 사람)

## 핵심 구조

세 역할이 한 묶음 — "재귀가 타입 체크 없이 흐르게 하기 위한 장치 세트"다.

**Component** — Leaf와 Composite 모두가 구현하는 공통 인터페이스.
- 같은 메서드를 강제하는 장치. 호출자가 둘을 구분 안 해도 되는 이유.
- 위 예제의 `get_size()` 시그니처가 여기 해당.

**Leaf** — 잎 노드. 자기 안에서 작업이 끝남. 위 예제에서는 `File`.
- 재귀의 종착점. `get_size()`가 자기 크기만 돌려주고 끝.

**Composite** — 자식들을 관리하는 복합 노드. 위 예제에서는 `Folder`.
- `add(component)` / `remove(component)` → 자식 관리
- `get_size()` → 자식들의 같은 메서드를 재귀 호출. 트리를 풀리게 하는 핵심.

### 재귀의 흐름

```
Folder.get_size()                    ← 호출자가 한 번 부름
    ├─ child1.get_size()             ← child가 File이면 여기서 종료
    └─ child2.get_size()             ← child가 Folder면 다시 자식들에게…
        └─ grandchild.get_size()
```

## Python 예제

→ `src/examples/composite_example.py`

## 주의할 점

### 투명성 vs 안전성 — `add()` / `remove()`를 어디에 둘까

폴더에는 `add(child)`가 필요한데 파일에는 필요 없다. 이 메서드를 **공통 인터페이스(Component)**에 넣을 것인가, **Composite에만** 둘 것인가? 두 선택은 서로 다른 가치를 양보한다.

**투명성 — Component에 넣기**

```python
class Component(ABC):
    @abstractmethod
    def get_size(self): ...
    def add(self, child): raise NotImplementedError   # 기본은 예외

class File(Component):
    def get_size(self): return self.bytes
    # add() 따로 구현 안 함 — 호출하면 예외

class Folder(Component):
    def add(self, child): self.children.append(child)

# 호출 — 타입 구분 불필요
node.add(new_file)   # Folder면 작동, File이면 런타임 예외
```

→ 호출자가 둘을 진짜 똑같이 다룸. 단, File에 `add()` 부르는 잘못된 호출이 **런타임에서야** 터짐.

**안전성 — Composite에만 두기**

```python
class Component(ABC):
    @abstractmethod
    def get_size(self): ...
    # add() 없음

class File(Component):
    def get_size(self): return self.bytes

class Folder(Component):
    def add(self, child): self.children.append(child)

# 호출 — 분기 필요
if isinstance(node, Folder):
    node.add(new_file)   # File에는 .add()가 아예 없으므로 타입 체커가 잡음
```

→ 잘못된 호출이 **타입 검사 단계에서** 차단됨. 단, 호출자가 다시 `isinstance` 분기를 떠안음.

**선택 기준**: GoF 책은 **투명성**을 더 권장한다. Composite 패턴 자체가 "둘을 구분 없이 다룬다"가 본질이기 때문. 단, 타입 안전이 중요한 도메인이면 안전성 쪽도 합리적.

### 그 외 주의점

- **과도한 일반화**: 단순한 리스트로 충분한 상황에 Composite를 쓰면 불필요한 복잡성이 생김. 재귀적 트리 구조가 명확할 때만 적용.
- **사이클 주의**: 자식이 부모를 다시 가리키면 재귀가 무한 루프에 빠진다. 양방향 참조가 필요하다면 별도의 사이클 방지 로직이 필요.
