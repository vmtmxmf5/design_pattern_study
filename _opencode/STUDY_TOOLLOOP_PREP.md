# Tool Loop 준비 단계 — LLM 호출 전에 벌어지는 4가지

`handle.process()`를 호출하기 전, 4가지를 준비해서 한꺼번에 넘긴다.

```python
# 4가지가 모여서 handle.process()에 전달된다
result = await handle.process(
    system=system,             # 1. 시스템 프롬프트
    tools=tools,               # 2. 도구 목록
    permission=permission,     # 3. 권한 규칙
    messages=model_msgs,       # 4. 메시지 히스토리
    ...
)
```

```typescript
// 실제 코드 (prompt.ts:1506~1526)
const [skills, env, instructions, modelMsgs] = yield* Effect.all([
  Effect.promise(() => SystemPrompt.skills(agent)),      // skill 목록
  Effect.promise(() => SystemPrompt.environment(model)), // 환경 정보
  instruction.system().pipe(Effect.orDie),                // CLAUDE.md 등
  Effect.promise(() => MessageV2.toModelMessages(msgs, model)), // 메시지 변환
])
const system = [...env, ...(skills ? [skills] : []), ...instructions]

const result = yield* handle.process({
  system,                          // 1. 시스템 프롬프트
  tools,                           // 2. 도구 목록
  permission: session.permission,  // 3. 권한 규칙
  messages: modelMsgs,             // 4. 메시지 히스토리
  user: lastUser,
  agent,
  model,
  sessionID,
})
```

---

## 1. 시스템 프롬프트 구성

LLM에게 "너는 이런 역할이야"를 알려주는 프롬프트를 조립한다. 세 가지를 합침.

```typescript
// prompt.ts:1506~1512
const [skills, env, instructions] = yield* Effect.all([
  Effect.promise(() => SystemPrompt.skills(agent)),       // 사용 가능한 skill 목록
  Effect.promise(() => SystemPrompt.environment(model)),  // OS, 작업 디렉토리, Git 여부 등
  instruction.system().pipe(Effect.orDie),                // CLAUDE.md, AGENTS.md 등 프로젝트 설정
])
const system = [...env, ...(skills ? [skills] : []), ...instructions]
```

```python
# Python 번역
skills = await SystemPrompt.skills(agent)          # 사용 가능한 skill 목록
env = await SystemPrompt.environment(model)        # OS, 작업 디렉토리, Git 여부 등
instructions = await instruction.system()          # CLAUDE.md, AGENTS.md 등 프로젝트 설정

system = [*env, skills, *instructions]             # 합쳐서 하나의 시스템 프롬프트로
```

---

## 2. 도구 목록 결정

LLM이 쓸 수 있는 도구를 에이전트 종류에 따라 결정한다.

- `build` agent → 거의 모든 도구 사용 가능
- `explore` agent → 읽기 전용 도구만 (grep, glob, read 등)
- `plan` agent → 편집 도구 차단

```typescript
// prompt.ts:386~
const resolveTools = Effect.fn("SessionPrompt.resolveTools")(function* (input) {
  const tools = {}

  // ToolRegistry에서 에이전트/모델에 맞는 도구들을 가져온다
  for (const item of yield* registry.tools({
    modelID: input.model.api.id,
    providerID: input.model.providerID,
    agent: input.agent,
  })) {
    tools[item.id] = tool({
      description: item.description,
      execute(args, options) {
        // 각 도구마다 context를 만들어서 실행
        // context에 sessionID, 권한 체크 함수(ask), 메타데이터 콜백 등이 포함됨
        const ctx = context(args, options)
        return item.execute(args, ctx)
      },
    })
  }
  return tools
})
```

```python
# Python 번역
async def resolve_tools(agent, model, session):
    tools = {}

    # 에이전트/모델에 맞는 도구들을 가져온다
    for item in registry.tools(model_id=model.id, agent=agent):
        tools[item.id] = Tool(
            description=item.description,
            execute=lambda args: item.execute(args, context={
                "session_id": session.id,
                "ask": permission.ask,  # 권한 체크 함수 주입
            })
        )
    return tools
```

---

## 3. 권한 체크

에이전트 권한 + 세션 권한을 **병합**해서, 도구 실행 전에 "이거 실행해도 되나?" 확인한다.

```
allow → 바로 실행
ask   → 사용자에게 물어봄
deny  → 차단
```

```typescript
// prompt.ts:423~431 (resolveTools 내부, 각 도구의 context에 주입됨)
ask: (req) =>
  permission.ask({
    ...req,
    sessionID: input.session.id,
    // 에이전트 권한 + 세션 권한을 병합
    ruleset: Permission.merge(input.agent.permission, input.session.permission ?? []),
  }),
```

```python
# Python 번역
# 도구가 실행될 때마다 이 함수가 호출된다
def ask(req):
    ruleset = Permission.merge(
        agent.permission,      # 에이전트 레벨 권한 (예: explore는 edit 차단)
        session.permission,    # 세션 레벨 권한 (예: 사용자가 추가한 규칙)
    )
    return permission.ask(
        req,
        session_id=session.id,
        ruleset=ruleset,
    )
    # ruleset에서 매칭되는 규칙을 찾아 allow/ask/deny 결정
```

---

## 4. 메시지 히스토리 정리

대화 기록을 LLM에게 보내기 전에 가공한다.

```typescript
// prompt.ts:1351 — 압축된 메시지 필터링
let msgs = yield* MessageV2.filterCompactedEffect(sessionID)

// prompt.ts:1486~1501 — 2번째 루프 이후, 사용자 메시지를 system-reminder로 감싸기
if (step > 1 && lastFinished) {
  for (const m of msgs) {
    if (m.info.role !== "user" || m.info.id <= lastFinished.id) continue
    for (const p of m.parts) {
      p.text = [
        "<system-reminder>",
        "The user sent the following message:",
        p.text,
        "Please address this message and continue with your tasks.",
        "</system-reminder>",
      ].join("\n")
    }
  }
}

// prompt.ts:1510 — 모델이 이해하는 형식으로 변환
const modelMsgs = yield* Effect.promise(() =>
  MessageV2.toModelMessages(msgs, model)
)
```

```python
# Python 번역

# 1) 압축된 오래된 메시지 필터링
msgs = await MessageV2.filter_compacted(session_id)

# 2) 2번째 루프 이후, 사용자 메시지를 감싸기
#    → LLM이 도구 실행 중에 사용자가 보낸 메시지를 놓치지 않게
if step > 1 and last_finished:
    for msg in msgs:
        if msg.role != "user":
            continue
        msg.text = f"""<system-reminder>
The user sent the following message:
{msg.text}
Please address this message and continue with your tasks.
</system-reminder>"""

# 3) 모델이 이해하는 형식으로 변환 (이미지 추출, 도구 결과 포맷팅 등)
model_msgs = await MessageV2.to_model_messages(msgs, model)
```
