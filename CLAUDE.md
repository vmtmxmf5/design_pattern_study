# CLAUDE.md

## Project
LLM Wiki 방식 디자인 패턴 스터디.
- `project_knowledge/` — 검토 완료된 스터디 노트
- `generated_docs/` — LLM 생성 문서 (검토 대기)
- `src/examples/` — 패턴별 실행 가능한 예제 코드
- `tests/` — 예제 실행 검증 테스트

## Rules
- 문서 언어: 한국어
- 코드 예제: Python (`src/examples/패턴명_example.py`)
- Lint: `ruff check .` (커밋 전 반드시 통과)
- 테스트: `pytest tests/` (커밋 전 반드시 통과)
- 문서 위치: `project_knowledge/패턴명.md` (검토 완료), `generated_docs/패턴명.md` (검토 대기)
- 예제 코드 수정 시 `python3 -m pytest tests/test_examples.py`로 검증할 것
- 프로젝트 구조나 설정 변경 시 반드시 사용자에게 확인을 받을 것
- 변경 사항이 있으면 `CLAUDE.md`, `README.md`, `pyproject.toml`도 함께 업데이트할 것
