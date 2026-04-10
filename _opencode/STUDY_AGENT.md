# Agent 레지스트리 — agent.ts

## 이 파일이 하는 일

에이전트를 **설정(permission, prompt, model 등)과 함께 등록하고, 이름으로 꺼내 쓸 수 있게 하는 레지스트리**.

기본 6개가 하드코딩돼 있고, 사용자 설정 파일로 수정/삭제/추가 가능하다.

```
agents = {
    "build":      { permission: 거의 전부, mode: "primary" },
    "plan":       { permission: 편집 차단, mode: "primary" },
    "general":    { permission: 거의 전부, mode: "subagent" },
    "explore":    { permission: 읽기만,   mode: "subagent" },
    "compaction": { permission: 전부 차단, mode: "primary", hidden: true },
    "title":      { permission: 전부 차단, mode: "primary", hidden: true },
    "summary":    { permission: 전부 차단, mode: "primary", hidden: true },
}

Agent.get("build")  → 에이전트 설정 반환
```

---

## 에이전트 분류

### Primary — 사용자 요청을 직접 처리

| 에이전트 | 역할 | permission 핵심 |
|---------|------|----------------|
| build | 기본 에이전트. 코드 읽기/수정/실행 다 가능 | 거의 전부 allow |
| plan | 계획만 세움. LLM이 성급하게 수정하는 걸 방지 | edit: deny |

### Subagent — primary에게 작업을 위임받아 처리

| 에이전트 | 역할 | permission 핵심 |
|---------|------|----------------|
| general | 범용. primary와 비슷하게 거의 다 가능 | 거의 전부 allow |
| explore | 코드베이스 탐색 전용. 읽기만 가능 | 8개 도구만 allow (grep, glob, list, bash, read, webfetch, websearch, codesearch) |

**왜 explore를 따로 만들었나?**
- **안전** — 도구를 읽기만 허용하므로 실수로 수정할 일이 없다
- **효율** — 도구 수가 적으면 LLM이 어떤 도구를 쓸지 빠르게 판단한다

### Hidden — 시스템 내부용 (사용자에게 안 보임)

| 에이전트 | 역할 |
|---------|------|
| compaction | 대화가 길어지면 이전 내용을 요약해서 컨텍스트를 줄인다 |
| title | 세션 제목 자동 생성 |
| summary | sub agent 작업 결과를 요약해서 primary에게 전달 |

이 셋은 전부 `"*": "deny"` — 도구를 쓸 필요 없이 텍스트만 받아서 텍스트를 뱉으면 된다.

---

## 에이전트 속성

```python
class AgentInfo:
    name: str            # 에이전트 이름 ("build", "explore" 등)
    description: str     # 설명
    mode: str            # "primary" | "subagent" | "all"
    permission: Ruleset  # 어떤 도구를 쓸 수 있는지 (allow/deny/ask)
    model: Model | None  # 어떤 LLM 모델을 쓸지 (없으면 기본값)
    prompt: str | None   # 시스템 프롬프트 ("넌 탐색 전문가야" 같은 것)
    temperature: float   # LLM 응답 창의성 (낮으면 보수적, 높으면 다양)
    hidden: bool         # 사용자에게 보이는지 여부
```

---

## 같은 구조, 다른 설정

모든 에이전트는 같은 `Info` 구조로 정의되고, 같은 `prompt() → runLoop()` 흐름을 탄다.
다만 **설정값 조합**이 달라서 행동이 달라진다:

```python
# 같은 구조, 다른 설정
build   = Info(permission=거의_전부, mode="primary",  prompt=None)
explore = Info(permission=읽기만,   mode="subagent", prompt="탐색 전문가")
plan    = Info(permission=편집차단, mode="primary",  prompt=None)
```

- permission에 따라 → 쓸 수 있는 도구가 달라짐
- prompt에 따라 → LLM 행동이 달라짐
- mode에 따라 → 직접 실행 or 위임받아 실행

---

## 레지스트리 패턴

에이전트를 이름(key)으로 등록하고, 이름으로 꺼내 쓴다.

```typescript
// agent.ts:107~234 — 에이전트 등록
const agents: Record<string, Info> = {
  build: { name: "build", permission: ..., mode: "primary" },
  plan:  { name: "plan",  permission: ..., mode: "primary" },
  // ...
}

// agent.ts:281~283 — 이름으로 꺼내기
const get = function* (agent: string) {
  return agents[agent]
}
```

```python
# Python 번역
# 에이전트 등록
agents = {
    "build": Info(name="build", permission=..., mode="primary"),
    "plan":  Info(name="plan",  permission=..., mode="primary"),
    # ...
}

# 이름으로 꺼내기
def get(agent: str) -> Info:
    return agents[agent]
```

**누가 쓰는가:**
- `get("build")` → tool loop이 에이전트 설정을 가져올 때
- `list()` → UI가 에이전트 목록을 보여줄 때
- `defaultAgent()` → 대화 시작 시 기본 에이전트 결정 (`build`)

---

## 사용자 커스터마이징

기본 6개 에이전트 외에, 설정 파일로 수정/삭제/추가할 수 있다.

```yaml
# 사용자 설정 파일 예시
agent:
  build:
    model: "claude-sonnet"        # 기존 에이전트의 모델 변경
    prompt: "너는 시니어 개발자야"  # 프롬프트 변경

  explore:
    disable: true                 # 기존 에이전트 비활성화(삭제)

  my-security-agent:              # 새 에이전트 추가
    description: "보안 전문가"
    prompt: "넌 보안 전문가야"
```

```typescript
// agent.ts:236~263 — 설정 파일로 덮어쓰기
for (const [key, value] of Object.entries(cfg.agent ?? {})) {
  if (value.disable) {
    delete agents[key]       // 비활성화 → 삭제
    continue
  }
  let item = agents[key]
  if (!item)
    item = agents[key] = {   // 없으면 새로 만듦
      name: key,
      mode: "all",
      permission: Permission.merge(defaults, user),
    }
  item.model = value.model ?? item.model       // 사용자 설정으로 덮어씀
  item.prompt = value.prompt ?? item.prompt
  item.description = value.description ?? item.description
  // ...
}
```

```python
# Python 번역
for key, value in config.agent.items():
    if value.disable:
        del agents[key]         # 비활성화 → 삭제
        continue

    item = agents.get(key)
    if item is None:
        item = agents[key] = Info(  # 없으면 새로 만듦
            name=key,
            mode="all",
            permission=Permission.merge(defaults, user),
        )

    item.model = value.model or item.model           # 사용자 설정으로 덮어씀
    item.prompt = value.prompt or item.prompt
    item.description = value.description or item.description
    # ...
```

---

## 전체 구조에서의 위치

```
사용자 → UI → defaultAgent() → "build"
                                   ↓
              tool loop ← Agent.get("build") → permission, prompt, model 꺼냄
                  ↓
              handle.process() → LLM 호출 (prompt 적용, permission으로 도구 필터링)
                  ↓
              sub agent 필요 → Agent.get("explore") → 새 세션에서 runLoop()
```
