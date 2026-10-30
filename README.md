# bracket-validator

Перевіряє, чи правильно закриті дужки у строці (стек на основі `list`).

- базовий режим: `()`
- розширений режим (за замовчуванням): `()`, `{}`, `<>`

```bash
pip install -i https://test.pypi.org/simple/ bracket-validator-mykola
bracket-validator
# або
python -m bracket_validator
```

```python
from bracket_validator import BracketValidator, ValidationError

BracketValidator().validate("<div><p>{ test }</p></div>")  # True
```
