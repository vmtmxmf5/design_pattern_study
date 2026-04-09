# Iterator Pattern

## 한 줄 정의

컬렉션의 내부 구조를 노출하지 않으면서, 요소를 하나씩 순회할 수 있는 통일된 방법을 제공하는 패턴.

## 언제 사용하는가

- **내부 구조가 다른 컬렉션을 동일한 방식으로 순회해야 할 때**: 리스트, 딕셔너리, 트리, 해시맵 등 서로 다른 자료구조를 하나의 인터페이스로 탐색하고 싶은 경우
- **컬렉션의 내부 구현을 숨기고 싶을 때**: 클라이언트가 배열인지 연결 리스트인지 몰라도 순회할 수 있어야 하는 경우
- **여러 종류의 순회 방식이 필요할 때**: 같은 컬렉션에 대해 정방향, 역방향, 필터링 순회 등 다양한 탐색 전략을 제공하고 싶은 경우
- **단일 책임 원칙을 지키고 싶을 때**: 컬렉션 클래스는 데이터 저장에만 집중하고, 순회 로직은 별도 Iterator 객체로 분리하고 싶은 경우

### 실제 사용 사례

- 식당 메뉴 통합 — Head First의 핵심 예제. Pancake House는 ArrayList로, Diner는 Array로 메뉴를 저장하는데, 웨이트리스(클라이언트)는 두 메뉴를 동일한 방식으로 순회해야 한다. Iterator를 도입해 내부 구현(ArrayList vs Array)을 감춤
- Python의 `__iter__`/`__next__` 프로토콜 (모든 for 루프의 기반)
- 데이터베이스 커서 (대량 결과를 한 행씩 가져오기)
- 파일 라인 읽기 (`for line in file`)

## 핵심 구조

**Iterator 생성** — 컬렉션은 자신의 내부 구조를 아는 Iterator 객체를 생성하여 반환한다.
- `Collection.create_iterator()` → `Iterator` 반환

**순회** — Iterator는 현재 위치를 추적하며 요소를 하나씩 꺼내준다.
- `Iterator.has_next()` → 다음 요소가 있는지 확인
- `Iterator.next()` → 다음 요소 반환 및 위치 이동

클라이언트는 Iterator 인터페이스만 사용하므로, 컬렉션이 리스트든 딕셔너리든 **동일한 코드로 순회**할 수 있다.

## Python 예제

```python
from abc import ABC, abstractmethod
from typing import Any


class Iterator(ABC):
    """반복자 인터페이스"""

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> Any:
        pass


class Collection(ABC):
    """컬렉션 인터페이스"""

    @abstractmethod
    def create_iterator(self) -> Iterator:
        pass


class Playlist:
    """리스트 기반 재생목록"""

    def __init__(self, name: str):
        self.name = name
        self._songs: list[str] = []

    def add_song(self, song: str) -> None:
        self._songs.append(song)

    def create_iterator(self) -> "PlaylistIterator":
        return PlaylistIterator(self._songs)


class PlaylistIterator(Iterator):
    """리스트를 순회하는 Iterator"""

    def __init__(self, songs: list[str]):
        self._songs = songs
        self._position = 0

    def has_next(self) -> bool:
        return self._position < len(self._songs)

    def next(self) -> str:
        song = self._songs[self._position]
        self._position += 1
        return song


class RecentPlays:
    """딕셔너리 기반 최근 재생 기록 (곡명 → 재생 횟수)"""

    def __init__(self):
        self._plays: dict[str, int] = {}

    def record(self, song: str) -> None:
        self._plays[song] = self._plays.get(song, 0) + 1

    def create_iterator(self) -> "RecentPlaysIterator":
        return RecentPlaysIterator(self._plays)


class RecentPlaysIterator(Iterator):
    """딕셔너리를 순회하는 Iterator"""

    def __init__(self, plays: dict[str, int]):
        self._items = list(plays.items())
        self._position = 0

    def has_next(self) -> bool:
        return self._position < len(self._items)

    def next(self) -> tuple[str, int]:
        item = self._items[self._position]
        self._position += 1
        return item


def print_all_songs(iterators: list[Iterator]) -> None:
    """내부 구조를 몰라도 동일한 방식으로 순회"""
    for iterator in iterators:
        while iterator.has_next():
            print(f"  ♪ {iterator.next()}")


# 사용
playlist = Playlist("운동할 때")
playlist.add_song("Eye of the Tiger")
playlist.add_song("Lose Yourself")
playlist.add_song("Stronger")

recent = RecentPlays()
recent.record("Bohemian Rhapsody")
recent.record("Hotel California")

print("--- 전체 곡 목록 ---")
print_all_songs([playlist.create_iterator(), recent.create_iterator()])
# ♪ Eye of the Tiger
# ♪ Lose Yourself
# ♪ Stronger
# ♪ ('Bohemian Rhapsody', 1)
# ♪ ('Hotel California', 1)
```

## 주의할 점

- **Python에는 이미 내장되어 있음**: `__iter__`와 `__next__`를 구현하면 for 루프에서 바로 사용 가능. 별도 Iterator 클래스를 만들기보다 Python 프로토콜을 활용하는 것이 자연스러움
- **순회 중 컬렉션 변경**: Iterator로 순회하는 도중에 원본 컬렉션이 변경되면 예측 불가능한 결과가 발생함 → 스냅샷을 찍거나 변경을 금지해야 함
- **단일 순회**: 기본 Iterator는 한 번 소진되면 재사용할 수 없음. 다시 순회하려면 새 Iterator를 생성해야 함
- **제너레이터 활용**: Python에서는 `yield`를 사용한 제너레이터가 Iterator 패턴의 간결한 대안이 됨
