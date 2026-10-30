"""Валідатор балансу дужок на основі стека."""

from typing import Dict, List, Optional, Sequence, Tuple

BASIC_BRACKETS: Dict[str, str] = {"(": ")"}
ADVANCED_BRACKETS: Dict[str, str] = {"(": ")", "{": "}", "<": ">"}


class ValidationError(ValueError):
    """Помилка валідації; `positions` — відсортовані індекси хибних дужок."""

    def __init__(self, message: str, positions: Sequence[int] = ()):
        super().__init__(message)
        self.positions: Tuple[int, ...] = tuple(positions)


class BracketValidator:
    def __init__(self, brackets: Optional[Dict[str, str]] = None):
        # відображення "відкриваюча -> закриваюча"
        self._open_to_close = dict(brackets or ADVANCED_BRACKETS)
        self._closing = set(self._open_to_close.values())

    def find_errors(self, text: str) -> List[int]:
        """Повертає відсортований список позицій хибних дужок."""
        stack: List[Tuple[str, int]] = []  # (відкриваюча дужка, індекс)
        errors: List[int] = []

        for idx, char in enumerate(text):
            if char in self._open_to_close:
                stack.append((char, idx))
            elif char in self._closing:
                if stack and self._open_to_close[stack[-1][0]] == char:
                    stack.pop()
                else:
                    errors.append(idx)  # зайва або не та закриваюча

        errors.extend(idx for _, idx in stack)  # так і не закриті
        return sorted(errors)

    def validate(self, text: str) -> bool:
        """True, якщо все ок; інакше ValidationError (підклас ValueError)."""
        errors = self.find_errors(text)
        if errors:
            positions = ", ".join(map(str, errors))
            raise ValidationError(
                f"Дужки незбалансовані на позиціях {positions}", errors
            )
        return True


def highlight(text: str, positions: Sequence[int]) -> str:
    """Рядок-підсвітка: `^` під кожною хибною дужкою."""
    marks = [" "] * len(text)
    for pos in positions:
        marks[pos] = "^"
    return "".join(marks).rstrip()
