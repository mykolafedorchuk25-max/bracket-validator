from .validator import BracketValidator, ValidationError, highlight


def main() -> None:
    input_text = input("Введіть строку: ")
    validator = BracketValidator()
    try:
        validator.validate(input_text)
    except ValidationError as err:
        print(input_text)
        print(highlight(input_text, err.positions))
        raise
    print("Строка валідна")


if __name__ == "__main__":
    main()
