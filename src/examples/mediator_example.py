"""Mediator Pattern 예제: 채팅방

사용자들이 서로 직접 메시지를 보내지 않고,
채팅방(Mediator)을 통해서만 소통하는 예제.
사용자는 다른 사용자의 존재를 모른다.
"""

from abc import ABC, abstractmethod


class ChatMediator(ABC):
    """채팅 중재자 인터페이스"""

    @abstractmethod
    def send_message(self, message: str, sender: "User") -> None:
        pass

    @abstractmethod
    def add_user(self, user: "User") -> None:
        pass


class User:
    """채팅 사용자 — Mediator만 알고, 다른 사용자는 모른다"""

    def __init__(self, name: str, mediator: ChatMediator):
        self.name = name
        self._mediator = mediator
        self.received: list[str] = []
        mediator.add_user(self)

    def send(self, message: str) -> None:
        """메시지를 Mediator에게 전달"""
        print(f"[{self.name}] 전송: {message}")
        self._mediator.send_message(message, sender=self)

    def receive(self, message: str, from_user: str) -> None:
        """Mediator가 전달해준 메시지를 수신"""
        msg = f"{from_user}: {message}"
        self.received.append(msg)
        print(f"  [{self.name}] 수신 <- {msg}")


class ChatRoom(ChatMediator):
    """채팅방 — 메시지를 발신자 외 모든 사용자에게 전달"""

    def __init__(self, name: str):
        self.name = name
        self._users: list[User] = []

    def add_user(self, user: User) -> None:
        self._users.append(user)
        print(f"[{self.name}] {user.name}님이 입장했습니다")

    def send_message(self, message: str, sender: User) -> None:
        """발신자를 제외한 모든 사용자에게 메시지 전달"""
        for user in self._users:
            if user is not sender:
                user.receive(message, from_user=sender.name)


if __name__ == "__main__":
    # 채팅방(Mediator) 생성
    room = ChatRoom("개발팀 채팅방")

    # 사용자들은 채팅방만 알고, 서로를 직접 참조하지 않음
    alice = User("Alice", room)
    bob = User("Bob", room)
    charlie = User("Charlie", room)

    print()
    alice.send("안녕하세요!")
    # [Alice] 전송: 안녕하세요!
    #   [Bob] 수신 <- Alice: 안녕하세요!
    #   [Charlie] 수신 <- Alice: 안녕하세요!

    print()
    bob.send("반갑습니다!")
    # [Bob] 전송: 반갑습니다!
    #   [Alice] 수신 <- Bob: 반갑습니다!
    #   [Charlie] 수신 <- Bob: 반갑습니다!
