# Proxy Pattern

## 한 줄 정의

실제 객체에 대한 접근을 대리 객체(Proxy)가 가로채서, 접근 제어나 부가 작업을 수행한 뒤 실제 객체에게 요청을 전달하는 패턴.

## 언제 사용하는가

- **무거운 객체의 생성을 미루고 싶을 때**: 대용량 이미지나 DB 커넥션처럼 생성 비용이 큰 객체를 실제로 필요한 시점까지 지연시킬 때 (가상 프록시)
- **접근 권한을 제어해야 할 때**: 사용자의 역할에 따라 특정 객체의 메서드 호출을 허용하거나 차단해야 할 때 (보호 프록시)
- **원격 객체를 로컬처럼 사용하고 싶을 때**: 다른 서버에 있는 객체를 마치 같은 프로세스에 있는 것처럼 호출하고 싶을 때 (원격 프록시)
- **부가 기능을 투명하게 끼워 넣고 싶을 때**: 캐싱, 로깅, 지연 로딩 등을 원본 객체 코드 변경 없이 추가해야 할 때
- **객체의 생명주기를 관리하고 싶을 때**: 참조 카운팅이나 리소스 해제 시점을 Proxy가 제어해야 할 때

### 실제 사용 사례

- 뽑기 기계 원격 모니터링 — Head First에서 State 패턴에 이어 등장. CEO가 원격지의 뽑기 기계 재고/상태를 모니터링하고 싶은데, Java RMI를 사용한 원격 프록시로 해결. 로컬 프록시 객체를 통해 원격 뽑기 기계를 마치 같은 프로세스에 있는 것처럼 호출
- ORM의 Lazy Loading (Django QuerySet이 실제 쿼리 실행을 지연)
- 웹 프록시 서버 (캐싱, 접근 제어)
- gRPC/RPC 클라이언트 스텁 (원격 서버 호출을 로컬 메서드처럼 사용)
- API Gateway (인증/인가 검사 후 실제 서비스에 요청 전달)

## 핵심 구조

**동일한 인터페이스** — Proxy는 실제 객체(RealSubject)와 같은 인터페이스를 구현한다. 클라이언트는 Proxy인지 실제 객체인지 구분하지 못한다.

**접근 가로채기** — 클라이언트의 요청이 Proxy를 먼저 거친다. Proxy는 접근 제어, 캐싱, 지연 생성 등 부가 작업을 수행한 뒤, 실제 객체에게 요청을 위임한다.

- `Client` → `Proxy.request()` 호출
- `Proxy` → 부가 작업 수행 (권한 검사, 캐시 확인, 객체 생성 등)
- `Proxy` → `RealSubject.request()` 위임

Decorator와 구조는 비슷하지만 목적이 다르다. Decorator는 기능을 추가하기 위해 감싸고, Proxy는 접근을 제어하기 위해 감싼다.

## Python 예제

```python
from abc import ABC, abstractmethod
import time


class ExternalAPI(ABC):
    """외부 API 호출 인터페이스"""

    @abstractmethod
    def fetch_data(self, query: str) -> dict:
        pass


class SlowExternalAPI(ExternalAPI):
    """실제 외부 API — 호출 비용이 비싸다"""

    def __init__(self, api_key: str):
        self._api_key = api_key
        print(f"API 클라이언트 초기화 (키: {api_key[:4]}****)")

    def fetch_data(self, query: str) -> dict:
        print(f"  [실제 API 호출] '{query}' 조회 중... (2초 소요)")
        time.sleep(2)  # 느린 외부 호출 시뮬레이션
        return {"query": query, "result": f"'{query}'에 대한 결과 데이터"}


class CachedAPIProxy(ExternalAPI):
    """캐싱 프록시 — 같은 요청은 캐시에서 바로 반환한다"""

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._real_api: SlowExternalAPI | None = None  # 지연 생성
        self._cache: dict[str, dict] = {}

    def _get_real_api(self) -> SlowExternalAPI:
        """실제 API 객체를 필요한 시점에 생성한다 (가상 프록시)"""
        if self._real_api is None:
            self._real_api = SlowExternalAPI(self._api_key)
        return self._real_api

    def fetch_data(self, query: str) -> dict:
        # 캐시에 있으면 실제 API를 호출하지 않는다
        if query in self._cache:
            print(f"  [캐시 히트] '{query}' → 즉시 반환")
            return self._cache[query]

        # 캐시에 없으면 실제 API에 위임
        result = self._get_real_api().fetch_data(query)
        self._cache[query] = result
        return result


class AuthAPIProxy(ExternalAPI):
    """보호 프록시 — 권한이 있는 사용자만 API를 호출할 수 있다"""

    def __init__(self, inner: ExternalAPI, allowed_roles: list[str]):
        self._inner = inner
        self._allowed_roles = allowed_roles
        self._current_role: str = "guest"

    def set_role(self, role: str) -> None:
        self._current_role = role

    def fetch_data(self, query: str) -> dict:
        if self._current_role not in self._allowed_roles:
            raise PermissionError(
                f"'{self._current_role}' 역할은 API 접근 권한이 없습니다"
            )
        print(f"  [권한 확인] '{self._current_role}' → 허용")
        return self._inner.fetch_data(query)


# 사용
# 1. 캐싱 프록시: 같은 요청을 반복해도 실제 호출은 한 번만 발생
api = CachedAPIProxy("sk-1234-secret-key")

print("=== 첫 번째 호출 ===")
result1 = api.fetch_data("서울 날씨")
# API 클라이언트 초기화 (키: sk-1****)     ← 이 시점에 실제 객체 생성
# [실제 API 호출] '서울 날씨' 조회 중... (2초 소요)

print("\n=== 같은 요청 반복 ===")
result2 = api.fetch_data("서울 날씨")
# [캐시 히트] '서울 날씨' → 즉시 반환     ← 캐시에서 즉시 반환

# 2. 보호 프록시: 권한 없는 사용자는 차단
print("\n=== 보호 프록시 ===")
protected_api = AuthAPIProxy(api, allowed_roles=["admin", "analyst"])

protected_api.set_role("guest")
try:
    protected_api.fetch_data("부산 날씨")
except PermissionError as e:
    print(f"  [차단] {e}")
# [차단] 'guest' 역할은 API 접근 권한이 없습니다

protected_api.set_role("admin")
result3 = protected_api.fetch_data("부산 날씨")
# [권한 확인] 'admin' → 허용
# [실제 API 호출] '부산 날씨' 조회 중... (2초 소요)
```

## 주의할 점

- **Decorator와의 혼동**: 구조가 거의 동일하지만 의도가 다르다. Proxy는 접근 제어가 목적이고, Decorator는 기능 추가가 목적이다. 의도에 맞게 이름을 짓자.
- **투명성 원칙**: 클라이언트는 Proxy를 쓰든 실제 객체를 쓰든 동일하게 동작해야 한다. Proxy가 인터페이스를 변경하면 안 된다.
- **과도한 프록시 체인**: Proxy를 여러 겹 쌓으면 디버깅이 어려워지고 응답 시간이 늘어날 수 있다.
- **캐시 무효화**: 캐싱 프록시를 사용할 때 캐시 만료 정책을 반드시 고려해야 한다. 오래된 데이터를 반환하는 것은 잘못된 결과보다 위험할 수 있다.
- **단순한 경우에는 불필요**: 접근 제어나 지연 로딩이 필요 없다면 Proxy를 도입할 이유가 없다. Python에서는 `__getattr__` 같은 매직 메서드로 간단히 해결 가능한 경우도 많다.
