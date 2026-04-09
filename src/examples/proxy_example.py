"""Proxy Pattern 예제: API 프록시

실제 객체에 대한 접근을 대리 객체(Proxy)가 가로채는 예제.
- CachedAPIProxy: 같은 요청은 캐시에서 바로 반환 (캐싱 + 가상 프록시)
- AuthAPIProxy: 권한이 있는 사용자만 API 호출 허용 (보호 프록시)
"""

from abc import ABC, abstractmethod


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
        print(f"  [실제 API 호출] '{query}' 조회 중...")
        return {"query": query, "result": f"'{query}'에 대한 결과 데이터"}


class CachedAPIProxy(ExternalAPI):
    """캐싱 프록시 — 같은 요청은 캐시에서 바로 반환"""

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._real_api: SlowExternalAPI | None = None  # 지연 생성
        self._cache: dict[str, dict] = {}

    def _get_real_api(self) -> SlowExternalAPI:
        """실제 API 객체를 필요한 시점에 생성 (가상 프록시)"""
        if self._real_api is None:
            self._real_api = SlowExternalAPI(self._api_key)
        return self._real_api

    def fetch_data(self, query: str) -> dict:
        # 캐시에 있으면 실제 API를 호출하지 않음
        if query in self._cache:
            print(f"  [캐시 히트] '{query}' -> 즉시 반환")
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
        print(f"  [권한 확인] '{self._current_role}' -> 허용")
        return self._inner.fetch_data(query)


if __name__ == "__main__":
    # 1. 캐싱 프록시
    api = CachedAPIProxy("sk-1234-secret-key")

    print("=== 첫 번째 호출 ===")
    api.fetch_data("서울 날씨")
    # API 클라이언트 초기화 (키: sk-1****)
    # [실제 API 호출] '서울 날씨' 조회 중...

    print("\n=== 같은 요청 반복 ===")
    api.fetch_data("서울 날씨")
    # [캐시 히트] '서울 날씨' -> 즉시 반환

    # 2. 보호 프록시
    print("\n=== 보호 프록시 ===")
    protected_api = AuthAPIProxy(api, allowed_roles=["admin", "analyst"])

    protected_api.set_role("guest")
    try:
        protected_api.fetch_data("부산 날씨")
    except PermissionError as e:
        print(f"  [차단] {e}")
    # [차단] 'guest' 역할은 API 접근 권한이 없습니다

    protected_api.set_role("admin")
    protected_api.fetch_data("부산 날씨")
    # [권한 확인] 'admin' -> 허용
    # [실제 API 호출] '부산 날씨' 조회 중...
