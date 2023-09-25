import urllib.parse


# Hex代表一个一位的16进制数字
class Hex:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        if self.val >= 10:
            return chr(self.val - 10 + ord('a'))
        else:
            return chr(ord('0') + self.val)

    def to_b(self):
        return "{:b}".format(self.val)

    @staticmethod
    def from_b(b):
        for c in b:
            if c != '0' and c != '1':
                raise ValueError("Hex.from_b() input must be a binary string, but found {}.".format(c))
        if not isinstance(b, str):
            raise TypeError("Hex.from_n() input must be a string.")
        if len(b) != 4:
            raise TypeError("Hex.from_n() input must be a int number.")
        val = 0
        for c in b:
            val = val * 2 + ord(c) - ord('0')
        return Hex(val)

    @staticmethod
    def from_n(n):
        if not isinstance(n, int):
            raise TypeError("Hex.from_n() input must be a int number.")
        if n >= 16 or n < 0:
            raise ValueError("Hex.from_n() input must be a num between 1 and 15, not {}".format(n))
        return Hex(n)

    # 从16进制的字符中获取值
    @staticmethod
    def from_h(h):
        if not isinstance(h, str) or len(h) != 1:
            raise TypeError("Hex.from_h() input must be a string with len()=1.")
        h=h.lower()
        if not (ord('0') <= ord(h[0]) <= ord('9') or ord('a') <= ord(h[0]) <= ord('f')):
            raise TypeError("Hex.from_h() input must be a string between 0-9 or a-f.")
        if ord('0') <= ord(h[0]) <= ord('9'):
            return Hex(ord(h[0])-ord('0'))
        else:
            return Hex(ord(h[0])+10-ord('a'))



# 二进制字符串转16进制字符串的列表
# 必须满足二进制字符串长度为4的整数倍
def b2h(string):
    if not isinstance(string, str):
        raise TypeError("b2h() input must be a string")
    n = 0
    hexs = []
    while n < len(string):
        hexs.append(Hex.from_b(string[n:n + 4]))
        n += 4
    return hexs


# 把字符串转化为16进制字符串的列表
# 由于字符串本身可能是被编码的,于是s2h指定了解码方法
# todo
def s2h(string):
    hexs = []
    i = 0
    while i < len(string):
        asc = ord(string[i])
        hexs.append(Hex.from_n(asc // 16))
        hexs.append(Hex.from_n(asc % 16))
        i += 1
    return hexs


# 把16进制字符串转为原字符串的列表
# 必须保证16进制字符串长度为2的整数倍
def h2s(string):
    res = []
    n = 0
    while n < len(string):
        res.append(chr(Hex.from_h(string[n]).val*16+Hex.from_h(string[n+1]).val))
        n+=2
    return res

def b2f(string):
    pass


# URL编码
url = "https://www.baidu.com/s?wd=ok"
print("".join(h2s("73646E6973635F32303138")))
# encoded_url = urllib.parse.quote(url,safe='')
# print("Encoded URL:", encoded_url)

# # URL解码
# decoded_url = urllib.parse.unquote(encoded_url)
# print("Decoded URL:", decoded_url)
