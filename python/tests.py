from main import str_to_list, convert


def test_str_to_list():
    print("START test_str_to_list")
    param = '1 asd 89 23'
    result = ['1', 'a', 's', 'd', '2', '3']
    response = str_to_list(param)
    assert response == result, f'FAILED test_str_to_list param=\'{param}\', assert {response} == {result}'
    print(f"[+] test param=\'{param}\', result={result}")

    param = '999999    hhh'
    result = ['h', 'h', 'h']
    assert str_to_list(param) == result, f'FAILED test_str_to_list param=\'{param}\', assert {response} == {result}'
    print(f"[+] test param=\'{param}\', result={result}")

    param = ''
    result = []
    assert str_to_list(param) == result, f'FAILED test_str_to_list param=\'{param}\', assert {response} == {result}'
    print(f"[+] test param=\'{param}\', result={result}")

    print("PASSED test_str_to_list")


def test_convert():
    print("START test_convert")
    param = 'CMXLIX'
    result = 949
    response = convert(param)
    assert response == result, f'FAILED test_convert param=\'{param}\', assert {response} == {result}'
    print(f"[+] test param=\'{param}\', result={result}")

    param = 'CML'
    result = 950
    assert convert(param) == result, f'FAILED test_convert param=\'{param}\', assert {response} == {result}'
    print(f"[+] test param=\'{param}\', result={result}")

    param = 'MMI'
    result = 2001
    assert convert(param) == result, f'FAILED test_convert param=\'{param}\', assert {response} == {result}'
    print(f"[+] test param=\'{param}\', result={result}")

    print("PASSED test_convert")


if __name__ == '__main__':
    test_str_to_list()
    test_convert()
