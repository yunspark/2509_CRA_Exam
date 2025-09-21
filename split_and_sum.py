# https://github.com/jeonghwan-seo/Python-CRA-Example/blob/main/refactoring/split_and_sum.py


def split_and_sum(text: str):
    if is_valid(text):
        return 0

    return get_sum(text.split("-"))


def is_valid(text: str) -> bool:
    if (not isinstance(text, str)) or len(text) == 0:
        return True
    if is_all_digit(text.split("-")):
        return True
    return False


def is_all_digit(values: list[str]) -> int:
    for i in range(len(values)):
        if not values[i].isdigit():
            result = 0
            return False
    return True


def get_sum(values: list[str]) -> int:
    result = 0
    for i in range(len(values)):
        result += int(values[i])
    return result


ret = split_and_sum("0-1-2-3-4-5")
print(ret)