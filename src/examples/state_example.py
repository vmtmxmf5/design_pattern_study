"""State Pattern 예제: 문서 승인 워크플로우"""

from abc import ABC, abstractmethod


class State(ABC):
    """문서 상태 인터페이스"""

    @abstractmethod
    def publish(self, doc: "Document") -> None:
        pass

    @abstractmethod
    def render(self, doc: "Document") -> str:
        pass


class DraftState(State):
    """초안 상태"""

    def publish(self, doc: "Document") -> None:
        print("검토 요청을 보냅니다.")
        doc.set_state(ModerationState())

    def render(self, doc: "Document") -> str:
        return f"[초안] {doc.content}"


class ModerationState(State):
    """검토 중 상태"""

    def publish(self, doc: "Document") -> None:
        if doc.current_user_role == "admin":
            print("관리자 승인 — 문서를 공개합니다.")
            doc.set_state(PublishedState())
        else:
            print("관리자만 승인할 수 있습니다.")

    def render(self, doc: "Document") -> str:
        return f"[검토중] {doc.content}"


class PublishedState(State):
    """공개 상태 — publish()를 호출해도 아무 일도 일어나지 않음"""

    def publish(self, doc: "Document") -> None:
        print("이미 공개된 문서입니다.")

    def render(self, doc: "Document") -> str:
        return f"[공개] {doc.content}"


class Document:
    """Context — 현재 상태에 모든 행동을 위임"""

    def __init__(self, content: str, user_role: str = "editor"):
        self.content = content
        self.current_user_role = user_role
        self._state: State = DraftState()

    def set_state(self, state: State) -> None:
        self._state = state

    def publish(self) -> None:
        self._state.publish(self)

    def render(self) -> str:
        return self._state.render(self)


if __name__ == "__main__":
    # 일반 편집자가 publish 시도
    doc = Document("디자인 패턴 가이드", user_role="editor")
    print(doc.render())      # [초안] 디자인 패턴 가이드

    doc.publish()             # 검토 요청을 보냅니다. → ModerationState로 전환
    print(doc.render())      # [검토중] 디자인 패턴 가이드

    doc.publish()             # 관리자만 승인할 수 있습니다. → 전환 안 됨

    # 관리자가 승인
    doc.current_user_role = "admin"
    doc.publish()             # 관리자 승인 — 문서를 공개합니다. → PublishedState로 전환
    print(doc.render())      # [공개] 디자인 패턴 가이드

    doc.publish()             # 이미 공개된 문서입니다.
