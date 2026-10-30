import pytest

from bracket_validator import (
    BASIC_BRACKETS,
    BracketValidator,
    ValidationError,
    highlight,
)


@pytest.fixture
def adv():
    return BracketValidator()


@pytest.fixture
def basic():
    return BracketValidator(BASIC_BRACKETS)


@pytest.mark.parametrize("text", ["", "abc", "()", "(())", "()()", "(a(b)c)"])
def test_basic_valid(basic, text):
    assert basic.validate(text) is True


@pytest.mark.parametrize(
    "text, expected",
    [("(", [0]), (")", [0]), ("(()", [0]), ("())", [2]), (")(", [0, 1])],
)
def test_basic_invalid(basic, text, expected):
    assert basic.find_errors(text) == expected
    with pytest.raises(ValueError):
        basic.validate(text)


def test_basic_ignores_other_brackets(basic):
    assert basic.validate("{<") is True


@pytest.mark.parametrize(
    "text", ["<div><p>{ test }</p></div>", "{<>}", "({<>})"]
)
def test_advanced_valid(adv, text):
    assert adv.validate(text) is True


def test_advanced_example_from_task(adv):
    text = "<div><p>{ test }}</p</div>"
    assert adv.find_errors(text) == [16, 17]
    with pytest.raises(ValidationError) as exc:
        adv.validate(text)
    assert str(exc.value) == "Дужки незбалансовані на позиціях 16, 17"
    assert exc.value.positions == (16, 17)


def test_wrong_pair(adv):
    assert adv.find_errors("(<)>") == [0, 2]


def test_highlight():
    assert highlight("abc}}", [3, 4]) == "   ^^"
    assert highlight("abc", []) == ""
