"""Iterator Pattern 예제: 음악 재생 목록

내부 구조가 다른 컬렉션(리스트 vs 딕셔너리)을
동일한 인터페이스로 순회하는 예제.
Python의 __iter__/__next__ 프로토콜도 함께 보여준다.
"""

from abc import ABC, abstractmethod
from typing import Any

# --- 직접 구현한 Iterator ---


class Iterator(ABC):
    """반복자 인터페이스"""

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> Any:
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
    """딕셔너리 기반 최근 재생 기록 (곡명 -> 재생 횟수)"""

    def __init__(self) -> None:
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


if __name__ == "__main__":
    # 리스트 기반 재생목록
    playlist = Playlist("운동할 때")
    playlist.add_song("Eye of the Tiger")
    playlist.add_song("Lose Yourself")
    playlist.add_song("Stronger")

    # 딕셔너리 기반 재생 기록
    recent = RecentPlays()
    recent.record("Bohemian Rhapsody")
    recent.record("Hotel California")

    # 내부 구조가 달라도 동일한 방식으로 순회
    print("--- 전체 곡 목록 ---")
    print_all_songs([playlist.create_iterator(), recent.create_iterator()])
    # ♪ Eye of the Tiger
    # ♪ Lose Yourself
    # ♪ Stronger
    # ♪ ('Bohemian Rhapsody', 1)
    # ♪ ('Hotel California', 1)
