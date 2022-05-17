##Example usage
```python
from main import str_to_list, convert

print(convert('VX'))
print(str_to_list('a  56 @. com999'))
```
```shell
15
['a', '5', '@', '.', 'c', 'o', 'm']
```


## Start test

```shell
python tests.py
```
```shell
START test_str_to_list
[+] test param='1 asd 89 23', result=['1', 'a', 's', 'd', '2', '3']
[+] test param='999999    hhh', result=['h', 'h', 'h']
[+] test param='', result=[]
PASSED test_str_to_list
START test_convert
[+] test param='CMXLIX', result=949
[+] test param='CML', result=950
[+] test param='MMI', result=2001
PASSED test_convert
```