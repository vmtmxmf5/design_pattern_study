# OpenCode Tool Loop 구조

## 왜 Tool Loop + Command 패턴인가?

LLM은 텍스트를 출력할 뿐, 직접 코드를 실행하거나 파일을 읽을 수 없다.
그래서 LLM의 텍스트 출력("파일 읽어줘")을 **Command 객체로 변환**해서 시스템이 대신 실행해야 한다.

- **왜 Command 객체로 변환하는가?**
  - 텍스트 그대로는 실행할 수 없다. 객체로 만들어야 `execute()`를 호출할 수 있다
  - 호출자(tool loop)는 도구의 내부 동작을 몰라도 된다 — 새 도구가 추가되어도 loop 코드를 수정할 필요 없음

- **왜 Loop인가?**
  - LLM은 한 번의 도구 실행으로 끝나지 않는다. 예: 파일을 읽고 → 내용을 보고 → 코드를 수정하고 → 결과를 확인한다
  - 매 실행마다 LLM이 결과를 받아 **다음에 뭘 할지 동적으로 결정**하므로, 미리 정해둘 수 없고 반복해야 한다
  - LLM이 더 이상 tool call을 하지 않으면 loop 종료

## 핵심 도식

```
사용자 → prompt() → run_loop()
                        │
                        ├─ 일반 도구 → 직접 실행
                        │
                        └─ sub agent → prompt() → run_loop()  ← 같은 구조 반복 (재귀)
```

- Primary agent와 sub agent는 같은 `prompt() → run_loop()` 흐름을 탄다
- 다만 sub agent는 **새 세션**에서 독립적으로 돌아간다
- 나머지는 전부 에러 처리, 권한 체크, 컨텍스트 압축 등 부가 로직

---

## 1단계: prompt() — 진입점

파일: `packages/opencode/src/session/prompt.ts:1308`

```typescript
// 사용자 메시지를 받아서 루프를 시작하는 진입점
// Primary agent든 sub agent든 여기를 통해 들어온다
const prompt = Effect.fn("SessionPrompt.prompt")(
  //                      ↑ 디버깅/로그용 이름표일 뿐, 입력값 아님
  function* (input: PromptInput) {
    const message = yield* createUserMessage(input)  // 사용자 메시지 저장
    return yield* loop({ sessionID: input.sessionID }) // run_loop 호출
  },
)
```

```python
# Python 번역
@trace(name="SessionPrompt.prompt")  # 로그용 이름표
async def prompt(input):
    message = await create_user_message(input)       # 사용자 메시지 저장
    return await loop(session_id=input.session_id)   # run_loop 호출
```

### Effect 읽는 법
- `yield*` = Python의 `await` (비동기 호출 끝날 때까지 기다림)
- `Effect.gen(function* () { ... })` = Python의 `async def`
- `Effect.fn("이름")` = 로그/디버깅용 이름표를 붙여서 함수 정의. 일반 함수 대신 Effect로 정의하는 이유: 나중에 **빌더 패턴**으로 `.pipe(retry, catch)` 같은 체이닝을 붙이려면 Effect 체계 안에서 정의해야 함

---

## 2단계: run_loop() — while(true) 무한 루프

파일: `packages/opencode/src/session/prompt.ts:1340`

```typescript
const runLoop = Effect.fn("SessionPrompt.run")(function* (sessionID) {
  let step = 0

  while (true) {
    let msgs = yield* MessageV2.filterCompactedEffect(sessionID)

    let lastUser, lastAssistant, lastFinished

    // ── 루프 종료 조건 ──
    if (lastAssistant?.finish
        && !["tool-calls"].includes(lastAssistant.finish)
        && lastUser.id < lastAssistant.id) {
      break
    }

    step++

    // ── sub agent 분기 ──
    const task = tasks.pop()
    if (task?.type === "subtask") {
      yield* handleSubtask({ task, model, lastUser, sessionID, session, msgs })
      continue
    }

    // ── 일반 도구 실행 (한 바퀴) ──
    const result = yield* handle.process({ user: lastUser, agent, system, messages, tools, model })

    if (result === "stop") break
    if (result === "compact") {
      yield* compaction.create({ sessionID, ... })  // 컨텍스트 압축
      continue  // 압축 후 다음 루프로
    }
    // "continue" → 다음 루프로
  }
})
```

```python
# Python 번역
async def run_loop(session_id):
    step = 0

    while True:
        # 메시지 히스토리 가져오기
        msgs = await get_messages(session_id)
        last_user = find_last_user_message(msgs)
        last_assistant = find_last_assistant_message(msgs)

        # ── 루프 종료 조건 ──
        # LLM이 끝났다고 했고, tool call이 아니면 → 종료
        if (last_assistant.finish
            and last_assistant.finish != "tool-calls"
            and last_user.id < last_assistant.id):
            break

        step += 1

        # ── sub agent 분기 ──
        task = tasks.pop()
        if task.type == "subtask":
            await handle_subtask(task, model, last_user, session_id, session, msgs)
            continue

        # ── 일반 도구 실행 (한 바퀴) ──
        result = await handle.process(
            user=last_user, agent=agent, system=system,
            messages=msgs, tools=tools, model=model
        )

        if result == "stop":
            break
        elif result == "compact":
            await do_compaction(session_id)
        # "continue" → 다음 루프로
```

---

## 3단계: handle.process() — LLM 호출 + 도구 실행 (한 바퀴)

파일: `packages/opencode/src/session/processor.ts:434`

### 도구 실행은 어디서 일어나는가?

`handle.process()`는 도구를 직접 실행하지 않는다.
2단계 run_loop에서 `tools`(사용 가능한 도구 목록)를 넘기면,
AI SDK(`streamText`)가 LLM 응답에 tool call이 있을 때 알아서 도구를 실행하고,
결과를 이벤트 스트림으로 돌려준다.
`handle.process()`는 그 이벤트를 받아서 **기록만** 한다.

```
run_loop이 tools를 넘김
        ↓
AI SDK (streamText)
        │
        ├─ LLM에게 메시지 보냄
        ├─ LLM 응답에 tool call 있으면 → 도구 찾아서 자동 실행
        ├─ tool-call 이벤트 발생
        ├─ tool-result 이벤트 발생
        ↓
handle.process()의 handle_event()가 이벤트를 받아서 상태 저장
```

### 코드

```typescript
const process = Effect.fn("SessionProcessor.process")(function* (streamInput) {
  const stream = llm.stream(streamInput)  // AI SDK에게 tools 포함해서 넘김

  yield* stream.pipe(
    Stream.tap((event) => handleEvent(event)),  // 이벤트 기록만 함
    Stream.takeUntil(() => ctx.needsCompaction),
    Stream.runDrain,
  ).pipe(
    Effect.onInterrupt(...),    // 중단됐을 때 처리
    Effect.retry(...),          // 실패하면 재시도
    Effect.catch(halt),         // 에러 잡기
    Effect.ensuring(cleanup()), // 무조건 마지막에 실행
  )

  if (ctx.needsCompaction) return "compact"
  if (ctx.blocked || ctx.assistantMessage.error) return "stop"
  return "continue"
})
```

```python
# Python 번역
# .pipe()는 빌더 패턴 — 비동기 실행 흐름을 체이닝으로 조립한다
# Effect로 함수를 정의했기 때문에 이런 체이닝이 가능

async def process(stream_input):
    # stream_input에 tools가 포함되어 있음
    # AI SDK가 LLM 응답에서 tool call 발견하면 알아서 실행하고
    # tool-call, tool-result 등의 이벤트를 스트림으로 내보냄

    result = await (
        llm.stream(stream_input)           # AI SDK에게 tools 포함해서 넘김
        .on_each(handle_event)             # 이벤트 받아서 기록만 함
        .stop_when(need_compaction)         # 조건 되면 멈춤
        .on_interrupt(handle_abort)         # 중단됐을 때 처리
        .retry(max=3)                       # 실패하면 재시도
        .on_error(halt)                     # 에러 잡기
        .finally_(cleanup)                  # 무조건 마지막에 실행
        .run()                              # 실행 (.build()에 해당)
    )

    if need_compaction: return "compact"
    if blocked or error: return "stop"
    return "continue"

def handle_event(event):
    if event.type == "tool-call":     # AI SDK가 도구 실행 시작함 → 상태 기록
    if event.type == "tool-result":   # AI SDK가 도구 실행 완료함 → 결과 저장
    if event.type == "tool-error":    # AI SDK가 도구 실행 실패함 → 에러 저장
    if event.type == "text-delta":    # LLM 텍스트 응답 스트리밍 → 화면 표시
    if event.type == "finish-step":   # 한 step 완료 → 토큰/비용 계산
```

핵심 이벤트 종류:
- `tool-call` → AI SDK가 도구 실행 시작함
- `tool-result` → AI SDK가 도구 실행 완료함, 결과 저장
- `tool-error` → 도구 실행 실패
- `text-delta` → LLM 텍스트 응답 스트리밍
- `finish-step` → 한 step 완료, 토큰/비용 계산

---

## 4단계: handleSubtask() → task_tool → prompt() — sub agent 재귀

파일: `packages/opencode/src/session/prompt.ts:552`

```typescript
const handleSubtask = Effect.fn("SessionPrompt.handleSubtask")(function* (input) {
  const result = yield* Effect.promise(() =>
    taskTool.execute({
      prompt: task.prompt,
      description: task.description,
      subagent_type: task.agent,
    }, ctx)
  )
})
```

```python
# Python 번역
async def handle_subtask(task, ctx):
    result = await task_tool.execute(
        prompt=task.prompt,
        description=task.description,
        subagent_type=task.agent,  # "explore", "general" 등
    )
```

파일: `packages/opencode/src/tool/task.ts:66~145`

```typescript
// task_tool 내부: 새 세션을 만들고 prompt()를 다시 호출한다
// 이것이 재귀의 핵심!
const nextSession = yield* Effect.promise(() =>
  Session.create({
    parentID: ctx.sessionID,
    title: params.description + ` (@${next.name} subagent)`,
  }),
)

const result = yield* Effect.promise(() =>
  SessionPrompt.prompt({
    sessionID: nextSession.id,
    agent: next.name,
    ...
  }),
)
```

```python
# Python 번역
# 새 세션을 만들고, prompt()를 다시 호출 → run_loop() 재귀!
next_session = await Session.create(
    parent_id=ctx.session_id,
    title=f"{params.description} (@{next.name} subagent)",
)

result = await prompt(                      # ← 1단계의 prompt()를 다시 호출!
    session_id=next_session.id,             # 새 세션에서
    agent=next.name,                        # sub agent로
)                                           # → prompt() → run_loop() 재귀
```

---

## 역할 정리 (Command 패턴 대입)

흐름: **Invoker → Command → Receiver**
- Invoker는 Command의 `execute()`를 호출하는 주체. 안에 뭐가 들어있는지 모르고, 그냥 실행만 한다
- Command는 함수 호출을 감싸는 객체. 실제 작업 대상인 Receiver를 가지고 있다
- Receiver는 Command가 실제로 일을 시키는 대상

| 역할 | 일반 예시 | OpenCode에서 | 파일 |
|------|----------|-------------|------|
| 손님 (Command 생성자) | 주문하는 손님 | LLM | - |
| Invoker (실행자) | 웨이트리스 — 주문서를 전달할 뿐, 요리법은 모름 | tool loop (`run_loop`) | `prompt.ts:1340` |
| Command (객체화된 요청) | 주문서 | tool call (파싱된 LLM 출력) | `processor.ts` |
| Receiver (실제 작업자) | 주방 — 실제로 요리하는 곳 | 파일시스템, 셸, LSP 등 | `tool/*.ts` |
