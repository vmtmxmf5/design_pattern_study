"""Decorator Pattern 예제: 함수 데코레이터

Python의 @데코레이터 문법을 활용해, 함수에 기능을 동적으로 추가하는 예제.
timer, retry, log_call 데코레이터를 겹겹이 감싸서 조합할 수 있다.
"""

import functools
import time


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
        print(f"[반환] {func.__name__} -> {result}")
        return result

    return wrapper


# 데코레이터를 겹겹이 감쌀 수 있다 — 핵심!
# 실행 순서: timer → retry → log_call → fetch_data
@timer
@retry(max_attempts=3)
@log_call
def fetch_data(url: str) -> str:
    """데이터를 가져오는 함수"""
    return f"{url}에서 데이터 수신 완료"


if __name__ == "__main__":
    result = fetch_data("https://api.example.com")
    # [호출] fetch_data(args=('https://api.example.com',), kwargs={})
    # [반환] fetch_data -> https://api.example.com에서 데이터 수신 완료
    # [fetch_data] 0.0001초 소요

    print(f"\n결과: {result}")
