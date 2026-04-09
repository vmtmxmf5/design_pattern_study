# Builder Pattern

## 한 줄 정의

메서드를 체이닝으로 호출해 객체를 조립하고, 완성된 객체만 반환하는 패턴

## 예시

```python
# 빌더 없이 — 불완전한 피자가 존재할 수 있음
pizza = Pizza()
pizza.dough = "thin"
# pizza.sauce 안 넣어도 pizza를 쓸 수 있음 → 위험

# 빌더 — .build() 전까지 Pizza 객체가 없음
pizza = (PizzaBuilder()
  .add_dough("thin")
  .add_sauce("tomato")
  .add_topping("cheese")
  .build())  # ← 이때 비로소 완성된 Pizza 반환
```

## 언제 사용하는가

- **불완전한 객체가 외부에 노출되면 안 될 때** — `.build()` 호출 전까지 객체가 생성되지 않으므로, 소스 없는 피자 같은 불완전한 상태를 방지
- **복합 객체를 단계적으로 구성해야 할 때** — 트리 구조나 중첩된 객체를 점진적으로 완성
- **같은 조립 과정으로 다른 결과물을 만들어야 할 때** — 같은 단계(도우→소스→토핑)로 마르게리따도, 페퍼로니도 만들 수 있다

### 실제 사용 사례

- SQL 쿼리 빌더 (`query.select("name").where("age > 20").order_by("name")`)
- 비동기 파이프라인 (Effect: `stream.retry(3).on_error(halt).finally(cleanup).run()`)

## 핵심 구조

**Builder** — 체이닝 메서드(`add_dough()`, `add_sauce()` 등)를 가진 조립 객체. 각 메서드는 자기 자신을 리턴해서 체이닝이 가능하다. `.build()`로 완성된 객체를 반환.

**Director (선택)** — 자주 쓰는 조립 순서를 미리 정해둔 함수/객체.

```python
# Director: 마르게리따 조립 순서를 재사용 가능하게 정해둔 것
def make_margherita(builder):
    builder.add_dough("thin")
    builder.add_sauce("tomato")
    builder.add_topping("mozzarella")
    return builder.build()

# 어디서든 한 줄로 마르게리따를 만들 수 있다
pizza = make_margherita(PizzaBuilder())
```

## Python 예제

→ `src/examples/builder_example.py`

## 주의할 점

- **단순한 객체에는 과함** — 파라미터가 3~4개뿐이면 생성자로 충분
- **Python에서는 키워드 인자로 대체 가능** — `dataclass`와 키워드 인자 조합이 Builder보다 간결한 경우가 많음
