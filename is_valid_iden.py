def is_valid_identifier(s: str) -> bool:
    """
    判断字符串 s 是否是合法的 Python 标识符。
    """
    return s.isidentifier()
print(is_valid_identifier('abc'))
print(is_valid_identifier('2abc'))