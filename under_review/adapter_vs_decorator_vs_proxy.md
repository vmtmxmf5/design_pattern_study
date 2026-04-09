# Adapter vs Decorator vs Proxy

셋 다 객체를 "감싸는" 구조 패턴이지만, **감싸는 이유**가 전혀 다르다.

## 핵심 차이

| 구분 | Adapter | Decorator | Proxy |
|------|---------|-----------|-------|
| **목적** | 인터페이스 변환 | 기능 추가 | 접근 제어 |
| **인터페이스** | 다른 인터페이스로 바꿈 | 같은 인터페이스 유지 | 같은 인터페이스 유지 |
| **감싸는 이유** | 안 맞는 걸 맞추려고 | 새 기능을 덧붙이려고 | 접근을 제어하려고 |
| **겹쳐 쓰기** | 보통 1개 | 여러 개 겹침 (핵심!) | 보통 1개 |

## 충전기로 비유하면

```
Adapter   = 110V → 220V 변환 어댑터. 플러그 모양을 바꿔줌
Decorator = 멀티탭. 콘센트 기능은 그대로인데, USB 충전 포트가 추가됨
Proxy     = 어린이 안전 커버. 콘센트는 그대로인데, 아이가 못 만지게 막음
```

## 판단 기준

```
감싸는 객체의 인터페이스를 바꾸나?
├── YES → Adapter (다른 인터페이스로 변환)
└── NO (같은 인터페이스 유지)
    ├── 기능을 추가하나? → Decorator
    └── 접근을 제어하나? → Proxy (캐싱, 권한, 지연 로딩 등)
```

## 코드로 보는 차이

```python
# Adapter: 인터페이스가 다른 SlackAPI를 NotificationSender에 맞춤
class SlackAdapter(NotificationSender):
    def send(self, to, msg):
        self._slack.post_message(channel=to, text=msg)  # 메서드 이름이 다름!

# Decorator: 같은 인터페이스에 로깅 기능 추가
@log_call      # send() → send() 그대로, 로깅만 추가
@timer         # 여러 개 겹칠 수 있음!
def send(to, msg): ...

# Proxy: 같은 인터페이스인데 권한 검사를 먼저 수행
class AuthProxy(ExternalAPI):
    def fetch_data(self, query):
        if self._role not in self._allowed:  # 접근 제어!
            raise PermissionError(...)
        return self._inner.fetch_data(query)
```
