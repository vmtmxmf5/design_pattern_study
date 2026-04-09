"""Chain of Responsibility Pattern 예제: 결재 시스템

금액에 따라 팀장 → 부장 → 이사 순으로 결재 권한을 확인하는 예제.
처리할 수 있는 사람이 나올 때까지 체인을 따라 요청이 전달된다.
"""

from abc import ABC, abstractmethod


class Approver(ABC):
    """결재자 인터페이스 — 다음 결재자에 대한 참조를 가짐"""

    def __init__(self, name: str, limit: int):
        self.name = name
        self.limit = limit
        self._next: Approver | None = None

    def set_next(self, approver: "Approver") -> "Approver":
        """다음 결재자 연결 — 체이닝 지원"""
        self._next = approver
        return approver

    def handle(self, amount: int, description: str) -> None:
        """결재 요청 처리 — 권한 내면 승인, 아니면 다음으로 전달"""
        if amount <= self.limit:
            self.approve(amount, description)
        elif self._next:
            print(f"  [{self.name}] {amount}만원은 권한 초과 → 다음으로 전달")
            self._next.handle(amount, description)
        else:
            print(f"  [반려] {amount}만원 '{description}' — 결재 가능한 사람이 없습니다")

    @abstractmethod
    def approve(self, amount: int, description: str) -> None:
        pass


class TeamLead(Approver):
    """팀장 — 100만원까지 결재 가능"""

    def approve(self, amount: int, description: str) -> None:
        print(f"  [{self.name} 승인] {amount}만원 '{description}'")


class Director(Approver):
    """부장 — 500만원까지 결재 가능"""

    def approve(self, amount: int, description: str) -> None:
        print(f"  [{self.name} 승인] {amount}만원 '{description}'")


class Executive(Approver):
    """이사 — 2000만원까지 결재 가능"""

    def approve(self, amount: int, description: str) -> None:
        print(f"  [{self.name} 승인] {amount}만원 '{description}'")


if __name__ == "__main__":
    # 체인 구성: 팀장 → 부장 → 이사
    team_lead = TeamLead("김팀장", limit=100)
    director = Director("박부장", limit=500)
    executive = Executive("이이사", limit=2000)

    team_lead.set_next(director).set_next(executive)

    # 다양한 금액의 결재 요청
    print("=== 결재 요청 ===")

    team_lead.handle(50, "사무용품 구매")
    # [김팀장 승인] 50만원 '사무용품 구매'

    print()
    team_lead.handle(300, "장비 구매")
    # [김팀장] 300만원은 권한 초과 → 다음으로 전달
    # [박부장 승인] 300만원 '장비 구매'

    print()
    team_lead.handle(1500, "서버 도입")
    # [김팀장] 1500만원은 권한 초과 → 다음으로 전달
    # [박부장] 1500만원은 권한 초과 → 다음으로 전달
    # [이이사 승인] 1500만원 '서버 도입'

    print()
    team_lead.handle(5000, "사옥 리모델링")
    # [김팀장] 5000만원은 권한 초과 → 다음으로 전달
    # [박부장] 5000만원은 권한 초과 → 다음으로 전달
    # [이이사] 5000만원은 권한 초과 → 다음으로 전달 (없음)
    # [반려] 5000만원 '사옥 리모델링' — 결재 가능한 사람이 없습니다
