# Design Pattern Study

LLM 기반 Wiki 방식의 디자인 패턴 스터디 자료 관리 프로젝트

## Overview

디자인 패턴을 학습하고, LLM을 활용하여 각 패턴에 대한 설명 자료(Markdown)를 자동 생성하는 시스템입니다.

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

## Structure

```
design_pattern_study/
├── README.md
├── CLAUDE.md
├── pyproject.toml
├── project_knowledge/   # 검토 완료된 스터디 노트
├── generated_docs/      # LLM 생성 문서 (검토 대기)
├── src/examples/        # 패턴별 실행 가능한 예제 코드
└── tests/               # 예제 실행 검증 테스트
```

### `project_knowledge/` - 검토 완료 스터디 노트

검토가 완료된 디자인 패턴 학습 자료를 관리하는 폴더입니다.

### `generated_docs/` - 검토 대기 문서

LLM이 자동 생성한 디자인 패턴 Wiki 문서가 저장되는 폴더입니다. 검토 후 `project_knowledge/`로 이동합니다.

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
