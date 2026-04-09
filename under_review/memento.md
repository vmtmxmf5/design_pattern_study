# Memento Pattern

## 한 줄 정의

객체의 내부 상태를 외부에 노출하지 않으면서 스냅샷(한 순간의 상태를 찍은 사진)으로 저장하고, 나중에 그 상태로 복원할 수 있게 하는 패턴.

## 언제 사용하는가

- **Undo/Redo 기능이 필요할 때**: 텍스트 에디터, 그래픽 도구 등에서 이전 상태로 되돌리기
- **트랜잭션 롤백이 필요할 때**: 작업이 실패하면 이전 상태로 복구해야 하는 경우
- **내부를 공개하지 않고 상태를 저장해야 할 때**: 내부 필드를 public으로 열지 않고도 스냅샷을 만들고 싶은 경우

### 실제 사용 사례

- 게임 세이브/로드 — 게임 엔진(Originator)이 체크포인트(Memento)를 만들어 저장
- 텍스트 에디터의 Undo 스택
- 데이터베이스 트랜잭션 롤백

## 핵심 구조

**Originator** — 상태를 가진 주인공 객체(예: 텍스트 에디터). 자신의 상태를 스냅샷으로 만들고, 스냅샷에서 복원할 수 있다.

**Memento** — 상태 스냅샷을 담는 불변 객체(예: 저장된 텍스트 내용). Originator만 내용에 접근할 수 있다.

**Caretaker** — Memento를 보관하는 관리자(예: Undo 히스토리 스택). Memento 내부를 열어보지 않고 보관만 한다.

- `Originator.save()` → `Memento` 생성
- `Originator.restore(memento)` → 저장된 상태로 복원
- `Caretaker` → Memento 리스트를 관리 (push/pop)

## Python 예제

→ `src/examples/memento_example.py`

## 주의할 점

- **메모리 소비**: 스냅샷을 자주 만들면 메모리가 빠르게 증가함 → 스냅샷 수 제한이나 diff 저장 고려
- **Python에서 불변성 보장 어려움**: Python에는 진정한 private이 없으므로 Memento 내부를 완벽히 보호하기 어려움
- **Command 패턴과 함께 사용**: Command의 `undo()` 구현 시 Memento로 이전 상태를 저장하는 조합이 일반적
