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

## Features

- LLM을 활용한 패턴 설명, 예제 코드, 사용 사례 생성
- 패턴별 실행 가능한 Python 예제 코드 제공
- Markdown 기반 스터디 자료 관리

### 개발 예정

- **코드에서 디자인 패턴 탐지**: 다른 프로젝트의 코드를 분석하여 디자인 패턴이 적용된 부분을 찾아내고, MD 문서로 자동 정리
- **디자인 패턴 기반 리팩토링**: 기존 코드에서 패턴 적용이 필요한 부분을 식별하고, `project_knowledge/`의 학습 자료를 기반으로 리팩토링 가이드 제공

## Structure

```
design_pattern_study/
├── README.md
├── CLAUDE.md
├── pyproject.toml
├── project_knowledge/   # 검토 완료된 스터디 노트
├── under_review/      # LLM 생성 문서 (검토 대기)
├── src/examples/        # 패턴별 실행 가능한 예제 코드
└── tests/               # 예제 실행 검증 테스트
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

### Creational Patterns (생성 패턴)
- Singleton, Factory Method, Abstract Factory, Builder, Prototype

### Structural Patterns (구조 패턴)
- Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy

### Behavioral Patterns (행동 패턴)
- Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor

### Other Patterns (기타 패턴)
- Registry, Event Bus
