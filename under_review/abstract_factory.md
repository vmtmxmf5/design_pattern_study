# Abstract Factory Pattern

## 한 줄 정의

서로 관련된 객체들을 한 세트로 묶어서, 세트 단위로 일관되게 생성하는 패턴. "다크 테마 세트" vs "라이트 테마 세트"처럼 관련 객체 군을 통째로 교체할 수 있다.

## 언제 사용하는가

- **관련 객체를 세트로 생성해야 할 때**: 버튼 + 체크박스 + 텍스트를 "Windows 스타일" 또는 "macOS 스타일"로 통일해서 만들어야 하는 경우
- **세트 내 객체 간 일관성이 중요할 때**: Windows 버튼에 macOS 체크박스가 섞이면 안 되는 경우
- **제품군을 통째로 교체해야 할 때**: 한 줄만 바꾸면 전체 UI 테마가 바뀌는 구조를 원하는 경우

### 실제 사용 사례

- GUI 프레임워크 — OS별로 다른 위젯 세트 생성 (Windows/macOS/Linux)
- 게임 맵 테마 — "숲" 테마면 나무+풀+돌, "사막" 테마면 선인장+모래+바위를 세트로 생성
- 데이터베이스 레이어 — PostgreSQL 세트(커넥션+쿼리빌더+마이그레이션) vs MySQL 세트

## 핵심 구조

**Abstract Factory** — 관련 객체들을 만드는 메서드 묶음을 정의한다.
- `create_button()`, `create_checkbox()` 같이 세트 내 각 객체 생성 메서드 제공

**Concrete Factory** — 특정 테마/스타일에 맞는 객체들을 실제로 생성한다.
- `DarkThemeFactory.create_button()` → 다크 버튼 반환
- `LightThemeFactory.create_button()` → 라이트 버튼 반환

클라이언트는 Abstract Factory 인터페이스만 사용하므로, Factory를 교체하면 세트 전체가 바뀐다.

## Python 예제

→ `src/examples/abstract_factory_example.py`

## 주의할 점

- **새로운 제품 종류 추가가 어려움**: 세트에 새 종류(예: 라디오 버튼)를 추가하면 모든 Factory를 수정해야 함
- **Factory Method와의 차이**: Factory Method는 객체 하나를 만들고, Abstract Factory는 관련 객체 세트를 만듦
- **Python에서는 간단하게 구현 가능**: 딕셔너리로 테마별 클래스 매핑을 관리하면 클래스 수를 줄일 수 있음
