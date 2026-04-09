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

- 디자인 패턴별 Wiki 스타일 문서 자동 생성
- LLM을 활용한 패턴 설명, 예제 코드, 사용 사례 생성
- Markdown 기반 스터디 자료 관리

## Structure

```
design_pattern_study/
├── README.md
├── CLAUDE.md
├── pyproject.toml
├── project_knowledge/   # 직접 작성하는 스터디 노트 / 참고 자료
├── generated_docs/      # LLM이 자동 생성한 패턴 설명 문서
└── src/                 # MD 문서 생성 코드
```

### `project_knowledge/` - 스터디 노트

직접 작성하거나 정리한 디자인 패턴 학습 자료를 관리하는 폴더입니다.

### `generated_docs/` - LLM 생성 문서

LLM이 자동 생성한 디자인 패턴 Wiki 문서가 저장되는 폴더입니다.
각 패턴별로 개념 설명, 구조(UML), 예제 코드, 실제 사용 사례 등을 포함합니다.

## Design Patterns

### Creational Patterns (생성 패턴)
- Singleton, Factory Method, Abstract Factory, Builder, Prototype

### Structural Patterns (구조 패턴)
- Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy

### Behavioral Patterns (행동 패턴)
- Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor
