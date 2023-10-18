import sys

from ._cfmt import cfmt
def write(*values):
    for v in values:
        sys.stdout.write(v)


def writef(fmt, *args):
    sys.stdout.write(cfmt(True, fmt, *args))


def writeln(fmt, *args):
    sys.stdout.write(cfmt(True, fmt, *args) + "\n")


def clear():
    sys.stdout.write("\33[2J")


def clear_line():
    to_linestart()
    clear_back()


def clear_back():  # 清除从光标到行尾的内容
    sys.stdout.write("\033[K")


def flush():
    sys.stdout.flush()


def to(x, y):  # 放置光标位置
    sys.stdout.write("\33[" + str(y) + ";" + str(x) + "H")


def to_linestart():
    sys.stdout.write("\r")


def up(n=1):
    sys.stdout.write("\33[" + str(n) + "A")


def down(n=1):
    sys.stdout.write("\033[" + str(n) + "B")


def right(n=1):
    sys.stdout.write("\33[" + str(n) + "C")


def left(n=1):
    sys.stdout.write("\33[" + str(n) + "D")


def hidden():  # 不显示光标
    sys.stdout.write("\33[?25l")


def show():  # 显示光标
    sys.stdout.write("\33[?25h")
