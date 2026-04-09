"""Builder Pattern 예제: 쿼리 빌더

복잡한 SQL 쿼리를 단계별로 조립하는 예제.
메서드 체이닝으로 읽기 쉽게 쿼리를 구성할 수 있다.
"""


class QueryBuilder:
    """SQL SELECT 쿼리를 단계별로 조립하는 빌더"""

    def __init__(self) -> None:
        self._table = ""
        self._columns: list[str] = []
        self._conditions: list[str] = []
        self._order_by: str = ""
        self._limit: int | None = None

    def table(self, name: str) -> "QueryBuilder":
        """FROM 테이블 지정"""
        self._table = name
        return self

    def select(self, *columns: str) -> "QueryBuilder":
        """SELECT 컬럼 추가"""
        self._columns.extend(columns)
        return self

    def where(self, condition: str) -> "QueryBuilder":
        """WHERE 조건 추가"""
        self._conditions.append(condition)
        return self

    def order(self, column: str) -> "QueryBuilder":
        """ORDER BY 지정"""
        self._order_by = column
        return self

    def limit_to(self, count: int) -> "QueryBuilder":
        """LIMIT 지정"""
        self._limit = count
        return self

    def build(self) -> str:
        """조립된 SQL 쿼리 문자열을 반환"""
        if not self._table:
            raise ValueError("테이블을 지정해야 합니다")

        cols = ", ".join(self._columns) if self._columns else "*"
        query = f"SELECT {cols} FROM {self._table}"

        if self._conditions:
            query += " WHERE " + " AND ".join(self._conditions)
        if self._order_by:
            query += f" ORDER BY {self._order_by}"
        if self._limit is not None:
            query += f" LIMIT {self._limit}"

        return query


if __name__ == "__main__":
    # 메서드 체이닝으로 쿼리 조립
    query = (
        QueryBuilder()
        .table("users")
        .select("name", "email")
        .where("age > 20")
        .where("active = true")
        .order("name")
        .limit_to(10)
        .build()
    )
    print(query)
    # SELECT name, email FROM users WHERE age > 20 AND active = true ORDER BY name LIMIT 10

    # 같은 빌더로 다른 쿼리도 조립 가능
    simple_query = QueryBuilder().table("products").build()
    print(simple_query)
    # SELECT * FROM products

    # 조건만 다른 쿼리
    filtered = (
        QueryBuilder()
        .table("orders")
        .select("id", "total")
        .where("status = 'pending'")
        .order("created_at")
        .build()
    )
    print(filtered)
    # SELECT id, total FROM orders WHERE status = 'pending' ORDER BY created_at
