# Decorator Pattern

## 한 줄 정의

기존 객체를 감싸는 래퍼(Wrapper) 객체를 통해, 원본 코드를 수정하지 않고 기능을 동적으로 추가하는 패턴.

## 언제 사용하는가

- **기존 클래스를 수정하지 않고 기능을 추가해야 할 때**: 원본 코드가 라이브러리에 있거나 변경이 위험한 경우
- **기능 조합이 다양할 때**: 상속으로 모든 조합을 만들면 클래스가 폭발적으로 늘어나는 경우 (예: 음료 + 토핑 조합)
- **런타임에 기능을 붙이거나 떼야 할 때**: 컴파일 시점이 아니라 실행 시점에 어떤 기능을 추가할지 결정해야 하는 경우
- **상속 대신 조합으로 확장하고 싶을 때**: 부모 클래스 변경 없이 새로운 행동을 유연하게 조합하고 싶은 경우

### 실제 사용 사례

- Java I/O 스트림 (`BufferedInputStream`이 `FileInputStream`을 감쌈)
- Python 데코레이터 (`@login_required`, `@cache`)
- 미들웨어 체인 (Django/Flask의 요청 처리 파이프라인)
- 음료 주문 시스템 (기본 음료 + 토핑 조합)

## 핵심 구조

**감싸기** — Decorator는 Component와 같은 인터페이스를 구현하면서, 내부에 Component를 가지고 있다. 덕분에 원본 대신 사용할 수 있다.

**위임 + 추가 동작** — Decorator는 감싼 객체에게 원래 작업을 위임하고, 그 전후에 자신만의 동작을 추가한다.

- `Decorator(component)` → 원본 객체를 감쌈
- `Decorator.operation()` → 자신의 동작 + `component.operation()` 호출

여러 Decorator를 겹겹이 감쌀 수 있어서, 기능을 자유롭게 조합할 수 있다.

## Python 예제

```python
import functools
import time


# --- @데코레이터 문법 활용 ---

def timer(func):
    """함수 실행 시간을 측정하는 데코레이터"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[{func.__name__}] {elapsed:.4f}초 소요")
        return result

    return wrapper


def retry(max_attempts: int = 3):
    """실패 시 재시도하는 데코레이터"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[{func.__name__}] 시도 {attempt}/{max_attempts} 실패: {e}")
                    if attempt == max_attempts:
                        raise

        return wrapper

    return decorator


def log_call(func):
    """함수 호출을 로깅하는 데코레이터"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[호출] {func.__name__}(args={args}, kwargs={kwargs})")
        result = func(*args, **kwargs)
        print(f"[반환] {func.__name__} → {result}")
        return result

    return wrapper


# 데코레이터를 겹겹이 감쌀 수 있다 — 핵심!
@timer
@retry(max_attempts=3)
@log_call
def fetch_data(url: str) -> str:
    return f"{url}에서 데이터 수신 완료"


fetch_data("https://api.example.com")
# [호출] fetch_data(args=('https://api.example.com',), kwargs={})
# [반환] fetch_data → https://api.example.com에서 데이터 수신 완료
# [fetch_data] 0.0001초 소요
```

## 주의할 점

- **클래스 수 증가**: Decorator마다 클래스를 만들어야 하므로, 소규모 프로젝트에서는 과할 수 있음
- **구체 타입 의존 금지**: 클라이언트가 원본의 구체 타입(`isinstance` 등)에 의존하면 Decorator가 끼어들었을 때 깨짐
- **생성 복잡도**: Decorator를 여러 개 감싸는 코드가 길어짐 → Factory나 Builder 패턴과 함께 쓰면 해결됨
- **디버깅 어려움**: 래퍼가 겹겹이 쌓이면 호출 흐름 추적이 복잡해짐
