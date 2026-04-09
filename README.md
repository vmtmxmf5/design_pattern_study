# Design Pattern Study

LLM 기반 Wiki 방식의 디자인 패턴 스터디 자료 관리 프로젝트

## Overview

디자인 패턴을 학습하고, 각 패턴에 대한 설명 자료와 실행 가능한 Python 예제를 관리하는 프로젝트입니다.

## Getting Started

### uv 설치

```bash
# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# pip로 설치
pip install uv
```

### 프로젝트 세팅

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 테스트 실행

```bash
# 전체 테스트
python3 -m pytest tests/

# 린트 검사
ruff check .
```

## Features

- LLM을 활용한 패턴 설명, 예제 코드, 사용 사례 생성
- 패턴별 실행 가능한 Python 예제 코드 제공
- Markdown 기반 스터디 자료 관리
- 헷갈리기 쉬운 패턴 간 비교 문서 제공

### 개발 예정

- **코드에서 디자인 패턴 탐지**: 다른 프로젝트의 코드를 분석하여 디자인 패턴이 적용된 부분을 찾아내고, MD 문서로 자동 정리
- **디자인 패턴 기반 리팩토링**: 기존 코드에서 패턴 적용이 필요한 부분을 식별하고, `project_knowledge/`의 학습 자료를 기반으로 리팩토링 가이드 제공

## Structure

```
design_pattern_study/
├── README.md
├── CLAUDE.md
├── pyproject.toml
├── requirements.txt         # 개발 의존성 (ruff, pytest)
├── project_knowledge/       # 검토 완료된 스터디 노트
├── under_review/            # LLM 생성 문서 (검토 대기)
├── src/examples/            # 패턴별 실행 가능한 예제 코드
└── tests/                   # 예제 실행 검증 테스트
```

### `project_knowledge/` - 검토 완료 스터디 노트

검토가 완료된 디자인 패턴 학습 자료를 관리하는 폴더입니다.

### `under_review/` - 리뷰 진행중

LLM이 생성한 디자인 패턴 문서가 리뷰를 거치는 폴더입니다. 검토 완료 후 `project_knowledge/`로 이동합니다.

### `src/examples/` - 예제 코드

각 패턴의 Python 예제를 실행 가능한 코드로 제공합니다. `python3 src/examples/패턴명_example.py`로 실행합니다.

### `tests/` - 테스트

`src/examples/` 내 모든 예제가 에러 없이 실행되는지 자동 검증합니다. `python3 -m pytest tests/`로 실행합니다.

## Design Patterns

### 검토 완료 (`project_knowledge/`)

| 패턴 | 예제 |
|------|------|
| Observer | `observer_example.py` |
| State | `state_example.py` |
| Strategy | `strategy_example.py` |
| State vs Strategy (비교) | — |

### 검토 대기 (`under_review/`)

| 분류 | 패턴 | 예제 |
|------|------|------|
| 생성 | Builder, Factory, Singleton | `builder_example.py`, `factory_example.py`, `singleton_example.py` |
| 구조 | Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy | `adapter_example.py`, `bridge_example.py`, `composite_example.py`, `decorator_example.py`, `facade_example.py`, `flyweight_example.py`, `proxy_example.py` |
| 행동 | Command, Iterator, Mediator, Memento, Template Method, Visitor | `command_example.py`, `iterator_example.py`, `mediator_example.py`, `memento_example.py`, `template_method_example.py`, `visitor_example.py` |
| 기타 | Event Bus, Registry | `event_bus_example.py`, `registry_example.py` |

### 비교 문서 (`under_review/`)

| 비교 | 핵심 차이 |
|------|-----------|
| Adapter vs Decorator vs Proxy | 인터페이스 변환 vs 기능 추가 vs 접근 제어 |
| Observer vs Mediator vs Event Bus | 일대다 알림 vs 양방향 조율 vs 완전 분리 발행/구독 |
| Factory vs Builder | 종류 선택 vs 단계별 조립 |
| Strategy vs Template Method | 조합으로 교체 vs 상속으로 교체 |
| Command vs Memento | 행동 캡슐화 vs 상태 스냅샷 |
| Facade vs Registry | 복잡한 과정을 묶기 vs 이름으로 찾기 |
| Singleton vs Registry | 인스턴스 1개 보장 vs 여러 객체 관리 |
| Composite vs Decorator | 트리 구조 vs 기능 래핑 |
