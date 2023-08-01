from enum import Enum

__color_map = {
    'b': 0,
    'r': 1,
    'g': 2,
    'y': 3,
    'u': 4,
    'p': 5,
    'c': 6,
    'a': 7,
    'x': 8
}

'''cfmt`{}`内的参数
冒号(:)前
    宽度:     指定字段的最小宽度,例如{:10}表示字段宽度为10个字符
    对齐方式:   指定字段的对齐方式,可选< 进行左对齐，> 进行右对齐, ^进行居中对齐.例如{:>10}表示右对齐,字段宽度为10个字符
    填充字符:   指定在宽度之前填充字段的字符,默认空格,可以使用任何字符作为填充字符,例如{:*<10}表示使用*字符进行左对齐填充
    精度:      仅适用于浮点数和某些其他类型,用于指定小数部分的位数或精度。例如{:.2f}表示保留两位小数
    数字前补0:  表示前补0(会考虑符号的长度),例如{:02}会将长度不足2的数字前补0
    数字符号:   传入+,例如{:+}会将结果中的正数显示+号

冒号(:)后
    假设k为代表某个颜色
    字体颜色:   {:k}代表字体颜色为k
    背景颜色:   {:_k}代表背景色为k
    字体加粗:   {:x}代表加粗(固定为字母x)

可以将各种效果重叠显示:
{10:y_rx}:      将字符串/数字按10位左对齐,颜色为加粗的红底黄色字体       
'''


def __add_color(source_string, color_string):
    res = "\033["
    i = 0
    while i < len(color_string):
        if color_string[i] == '_' and i + 1 < len(color_string):
            color = __color_map.get(color_string[i + 1], None)
            if color is not None and color != 8:
                res += str(color + 40) + ";"
            i += 2
        else:
            color = __color_map.get(color_string[i], None)
            if color is not None:
                if color == 8:
                    res += str(1) + ";"
                else:
                    res += str(color + 30) + ";"
            i += 1

    res = res[0:len(res) - 1] + "m"
    return res + source_string + "\033[0m"


def cfmt(use_color, _format, *args):
    n = len(_format)
    i = 0
    res = ""
    while i < n:
        if _format[i] == '\\' and i + 1 < len(_format):
            res += str(_format[i + 1])
            i += 2
            continue
        if _format[i] == '{':
            j = i + 1
            while j < n and _format[j] != '}':  # 找到 }
                j += 1
            if j < n:
                spl = _format[i + 1:j].split(":")
                if use_color and len(spl) == 2:
                    res += __add_color("{:" + spl[0] + "}", spl[1])
                else:
                    res += "{:" + spl[0] + "}"
            i = j + 1
        else:
            res += str(_format[i])
            i += 1
    return res.format(*args)
