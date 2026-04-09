"""Memento Pattern 예제: 텍스트 에디터

텍스트 에디터의 상태를 스냅샷으로 저장하고,
Undo로 이전 상태를 복원하는 예제.
Memento 내부는 에디터만 접근할 수 있다.
"""


class EditorMemento:
    """에디터 상태 스냅샷 (Memento) — 불변 객체"""

    def __init__(self, content: str, cursor_position: int):
        self._content = content
        self._cursor_position = cursor_position

    @property
    def content(self) -> str:
        return self._content

    @property
    def cursor_position(self) -> int:
        return self._cursor_position


class TextEditor:
    """텍스트 에디터 (Originator) — 상태를 저장/복원할 수 있다"""

    def __init__(self) -> None:
        self._content = ""
        self._cursor_position = 0

    def type_text(self, text: str) -> None:
        """텍스트 입력"""
        self._content += text
        self._cursor_position = len(self._content)
        print(f"[입력] '{text}' → 현재 내용: '{self._content}'")

    def delete_last(self, count: int = 1) -> None:
        """마지막 글자 삭제"""
        self._content = self._content[:-count]
        self._cursor_position = len(self._content)
        print(f"[삭제] {count}글자 → 현재 내용: '{self._content}'")

    def save(self) -> EditorMemento:
        """현재 상태를 스냅샷으로 저장"""
        print(f"[저장] 스냅샷 생성: '{self._content}'")
        return EditorMemento(self._content, self._cursor_position)

    def restore(self, memento: EditorMemento) -> None:
        """스냅샷에서 상태 복원"""
        self._content = memento.content
        self._cursor_position = memento.cursor_position
        print(f"[복원] 상태 복원: '{self._content}'")

    @property
    def content(self) -> str:
        return self._content


class History:
    """히스토리 관리자 (Caretaker) — Memento를 보관하지만 내부를 열어보지 않는다"""

    def __init__(self, editor: TextEditor):
        self._editor = editor
        self._snapshots: list[EditorMemento] = []

    def save(self) -> None:
        """현재 상태를 히스토리에 추가"""
        self._snapshots.append(self._editor.save())

    def undo(self) -> None:
        """마지막 저장 상태로 복원"""
        if not self._snapshots:
            print("[Undo] 되돌릴 상태가 없습니다")
            return
        memento = self._snapshots.pop()
        self._editor.restore(memento)


if __name__ == "__main__":
    editor = TextEditor()
    history = History(editor)

    # 텍스트 입력하면서 중간중간 저장
    editor.type_text("Hello")
    history.save()  # "Hello" 저장

    editor.type_text(", World")
    history.save()  # "Hello, World" 저장

    editor.type_text("!!!")
    print(f"\n현재 내용: '{editor.content}'")
    # 현재 내용: 'Hello, World!!!'

    # Undo: 마지막 저장 상태로 복원
    print("\n=== Undo ===")
    history.undo()
    # [복원] 상태 복원: 'Hello, World'

    history.undo()
    # [복원] 상태 복원: 'Hello'

    print(f"\n최종 내용: '{editor.content}'")
    # 최종 내용: 'Hello'
