"""Abstract Factory Pattern 예제: UI 테마

다크 테마와 라이트 테마의 UI 컴포넌트(버튼, 체크박스)를
세트 단위로 일관되게 생성하는 예제.
Factory를 교체하면 전체 테마가 바뀐다.
"""

from abc import ABC, abstractmethod

# --- Product: UI 컴포넌트들 ---


class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class DarkButton(Button):
    def render(self) -> str:
        return "[다크 버튼: 흰 글씨 + 어두운 배경]"


class DarkCheckbox(Checkbox):
    def render(self) -> str:
        return "[다크 체크박스: ☑ 흰색]"


class LightButton(Button):
    def render(self) -> str:
        return "[라이트 버튼: 검은 글씨 + 밝은 배경]"


class LightCheckbox(Checkbox):
    def render(self) -> str:
        return "[라이트 체크박스: ☑ 검정]"


# --- Abstract Factory ---


class UIFactory(ABC):
    """UI 컴포넌트 세트를 만드는 팩토리 인터페이스"""

    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass


class DarkThemeFactory(UIFactory):
    """다크 테마 세트"""

    def create_button(self) -> Button:
        return DarkButton()

    def create_checkbox(self) -> Checkbox:
        return DarkCheckbox()


class LightThemeFactory(UIFactory):
    """라이트 테마 세트"""

    def create_button(self) -> Button:
        return LightButton()

    def create_checkbox(self) -> Checkbox:
        return LightCheckbox()


# --- 클라이언트 코드 ---


def build_ui(factory: UIFactory) -> None:
    """Factory만 알면 됨 — 어떤 테마인지 몰라도 UI 생성 가능"""
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    print(f"  버튼: {button.render()}")
    print(f"  체크박스: {checkbox.render()}")


if __name__ == "__main__":
    print("=== 다크 테마 ===")
    build_ui(DarkThemeFactory())
    # 버튼: [다크 버튼: 흰 글씨 + 어두운 배경]
    # 체크박스: [다크 체크박스: ☑ 흰색]

    print("\n=== 라이트 테마 ===")
    build_ui(LightThemeFactory())
    # 버튼: [라이트 버튼: 검은 글씨 + 밝은 배경]
    # 체크박스: [라이트 체크박스: ☑ 검정]

    # Factory를 바꾸면 세트 전체가 바뀐다!
