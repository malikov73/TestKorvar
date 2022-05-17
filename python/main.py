from typing import List
import re


def str_to_list(param: str) -> List[str]:
    """
    function with one parameter of type string, that returns a list containing the characters of the parameter.
    If a character in the string is a space or a digit greater than 5,
    remove them and do not include them in the array
    """
    return [c for c in re.sub("[6-9\s]", "", param)]


def convert(param: str) -> int:
    """
    Convert roman numerals to integers.
    Works only with valid data!
    example: param='IIII' is valid.
             param='IIIII' is not valid.
    """
    roman = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    numbers = 0
    for i in range(len(param) - 1, -1, -1):
        num = roman[param[i]]
        if 3 * num < numbers:
            numbers = numbers - num
        else:
            numbers = numbers + num
    return numbers


if __name__ == "__main__":
    print(convert("VX"))
    print(str_to_list("a  56 @. com999"))
