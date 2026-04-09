"""Prototype Pattern 예제: 게임 캐릭터 복제

기본 스탯이 설정된 원형 캐릭터를 복제(clone)해서,
이름/위치만 바꿔 여러 캐릭터를 빠르게 만드는 예제.
"""

import copy


class Character:
    """게임 캐릭터 — 복제 가능"""

    def __init__(self, name: str, hp: int, attack: int, skills: list[str]):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.skills = skills

    def clone(self) -> "Character":
        """깊은 복사로 완전히 독립된 복제본 생성"""
        return copy.deepcopy(self)

    def show(self) -> None:
        print(f"  [{self.name}] HP={self.hp}, 공격력={self.attack}, 스킬={self.skills}")


if __name__ == "__main__":
    # 원형(Prototype) 생성 — 기본 스탯 설정
    warrior_proto = Character("전사 원형", hp=200, attack=30, skills=["베기", "방어"])

    # 원형을 복제해서 새 캐릭터 생성 — 처음부터 만들 필요 없음
    warrior1 = warrior_proto.clone()
    warrior1.name = "용사 1호"

    warrior2 = warrior_proto.clone()
    warrior2.name = "용사 2호"
    warrior2.skills.append("돌진")  # 이 캐릭터에만 스킬 추가

    print("=== 캐릭터 목록 ===")
    warrior_proto.show()
    warrior1.show()
    warrior2.show()
    # [전사 원형] HP=200, 공격력=30, 스킬=['베기', '방어']
    # [용사 1호] HP=200, 공격력=30, 스킬=['베기', '방어']
    # [용사 2호] HP=200, 공격력=30, 스킬=['베기', '방어', '돌진']

    # deepcopy이므로 복제본 수정이 원본에 영향 없음
    print(f"\n원형 스킬: {warrior_proto.skills}")
    print(f"2호 스킬: {warrior2.skills}")
    # 원형 스킬: ['베기', '방어']         ← 원본은 그대로
    # 2호 스킬: ['베기', '방어', '돌진']  ← 복제본만 변경됨
