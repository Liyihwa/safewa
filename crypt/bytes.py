import base64
import logwa


class Bytes:
    def __init__(self, data=bytearray()):
        self.data = data

    def __str__(self):
        return self.to_string()

    def __getitem__(self, item):
        return self.data[item]

    # ===================================
    def clone(self):
        return Bytes(self.data[:])

    def print(self, code="ascii"):
        print(self.to_string(code))

    def to_string(self, code="ascii"):
        return self.data.decode(code)

    # ===================================
    def hex_encode(self):
        return self.data.hex()

    def to_hex_list(self):
        self.print("utf8")
        return list(self.data.hex())

    def hex_decode(self):
        print(self.to_string("ascii"))
        return Bytes(bytearray.fromhex(self.to_string("ascii")))

    # ===================================
    # 从仅包含01的字符串中创建Bytes
    def bin_decode(self):
        byte_array = bytearray(int(self.data[i:i + 8], 2) for i in range(0, len(self.data), 8))
        return Bytes(byte_array)

    def to_bin_list(self):
        res = [] * (len(self.data) * 8)
        i = 0
        while i < len(self.data):
            b = bin(self.data[i])
            res[i * 8:i * 8 + 8] = b
            i += 1
        return res

    def bin_encode(self):
        return "".join(self.to_bin_list())

    # ======================================
    # 进行栅栏加密并返回加密后bytes,该函数会以byte为单位进行排序重组
    # 以字符为单位: todo
    def fence_encode(self, size):
        res = Bytes.init_with_size(len(self.data))
        k = 0
        for i in range(0, size):
            j = i
            while j < len(self.data):
                res.data[k] = self.data[j]
                j += size
                k += 1
        return res

    # 进行栅栏加密并返回加密后bytes,该函数会以byte为单位进行排序重组
    # 以字符为单位: todo
    def fence_decode(self, size):
        res = Bytes.init_with_size(len(self.data))
        k = 0
        for i in range(0, size):
            j = i
            while j < len(self.data):
                res.data[j] = self.data[k]
                j += size
                k += 1
        return res

    # ======================================
    def caesar_decode(self, key):
        return self.caesar_encode(26 - key)

    def caesar_encode(self, key):
        key = (key % 26 + 26) % 26
        s = self.to_nums_list()
        for i in range(0, len(s)):
            if ord('a') <= s[i] <= ord('z'):
                s[i] = (s[i] - ord('a') + key) % 26 + ord('a')
            elif ord('A') <= s[i] <= ord('Z'):
                s[i] = (s[i] - ord('A') + key) % 26 + ord('A')
        return Bytes.from_nums(s)

    # =======================================
    # 摩斯加密仅支持字母,数字
    __std_code = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
        '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
        '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
        '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
        '-.--': 'Y', '--..': 'Z', '.----': '1', '..---': '2', '...--': '3',
        '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
        '----.': '9', '-----': '0', '/': ' ',
        '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'", '-.-.--': '!',
        '-..-.': '/', '-.--.': '(', '-.--.-': ')', '.-...': '&', '---...': ':',
        '-.-.-.': ';', '-...-': '=', '.-.-.': '+', '-....-': '-', '..--.-': '_',
        '.-..-.': '"', '...-..-': '$', '.--.-.': '@',
    }


    __morse_code = {value: key for key, value in __std_code.items()}

    def morse_encode(self, point='.', line='-', ch_seg="/", alert=False):
        res = []

        for it in self.data:
            if ord('a') <= it <= ord('z'):
                it = chr(it - ord('a') + ord('A'))
            else:
                it = chr(it)
            res.append(Bytes.__morse_code[it].replace(".", point).replace("-", line) + ch_seg)
        return Bytes.from_string("".join(res)[:-len(ch_seg)])

    # todo 使用哈夫曼树优化
    def morse_decode(self, point='.', line='-', ch_seg="/", alert=False):
        sps = str(self)
        if point != '.':
            sps = sps.replace(point, '.')
        if line != '-':
            sps = sps.replace(line, '-')
        res = []

        for it in sps.split(ch_seg):
            if it not in Bytes.__std_code:
                if alert:
                    raise Exception("{} Match error".format(it))
                else:
                    res.extend(it)
            else:
                res.append(Bytes.__std_code[it])

        return Bytes.from_string("".join(res))

    # =======================================
    def base64_decode(self):
        return Bytes(base64.b64decode(self.data))

    def base64_encode(self):
        return Bytes(base64.b64encode(self.data))

    def base32_decode(self):
        return Bytes(base64.b32decode(self.data))

    def base32_encode(self):
        return Bytes(base64.b32encode(self.data))

    # =======================================
    def url_encode(self, encode_all=False):
        if len(self.data) == 0:
            return ""
        h = self.to_hex_list()
        url = "%" + "%".join(["".join(h[i:i + 2]) for i in range(0, len(h), 2)])

        return Bytes.from_string(url)

    def url_decode(self):
        res = []
        i = 0
        while i < len(self.data):
            if self.data[i] == ord('%'):
                res.append(int((self.data[i + 1:i + 3].decode("ascii")), 16))
                i += 3
            else:
                res.append(self.data[i])
                i += 1
        return Bytes(bytearray(res))

    # =======================================
    '''将Bytes视为 外表为unicode的字符串,并进行unicode_escape解码
        例如字符串 r"\u4e2d\u56fd"
        经过该decode方法后,得到b"\\u4e2d\\u56fd"的Bytes
    '''

    def unicode_decode(self):
        s = eval('"' + self.to_string() + '"')
        return Bytes.from_string(s, "unicode_escape")

    '''将unicode_escape解码为 unicode字符串
        例如将 b"\u4e2d\u56fd" 编码为 r"\u4e2d\u56fd"        
    '''

    def unicode_encode(self):
        s = eval('r"' + self.to_string() + '"')
        return Bytes.from_string(s)

    # =======================================
    def to_ascii_list(self, join=None):
        if join != None:
            return join.join([chr(int(b)) for b in self.data if int(b) < 128])
        else:
            return [chr(int(b)) for b in self.data if int(b) < 128]

    # =======================================
    @staticmethod
    def from_string(string, code="ascii"):
        return Bytes(bytearray(string.encode(code)))

    @staticmethod
    def from_nums(nums):
        return Bytes(bytearray(nums))

    def to_nums_list(self):
        return [int(b) for b in self.data]

    @staticmethod
    def init_with_size(size):
        return Bytes(bytearray(size))

    @staticmethod
    def from_file(filename):
        file = open(filename, mode='rb')
        rt = Bytes(bytearray(file.read()))
        file.close()
        return rt


if __name__ == '__main__':
    logwa.std_on(logwa.level_only_config())
