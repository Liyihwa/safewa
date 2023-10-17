import time

'''
https://zhuanlan.zhihu.com/p/111022726

返回该timestamp对应的持续时间是多久
该方法不够精确,在毫秒级别上误差比较大,如需精确表示,建议采用: perf_counter()方法
可接受的format元素有:
%d  日
%H  时
%M  分
%S  秒
%f  毫秒
%%  %字符

假设timestamp为1小时20分
format=%M的话,则结果为80
format=%H的话,结果为1
使用时请按照foramt时间单位从大到小的顺序,日时分秒 毫秒

'''


class Time:
    __time_item = (
        ('d', 24 * 60 * 60 * 1000), ('H', 60 * 60 * 1000), ('M', 60 * 1000), ('S', 1000), ('u', 1))

    def __init__(self, timestamp):  # cst北京时间
        self.timestamp = timestamp

    # time.strftime目的是将时间戳转为字符串,但是需要用到当地时区,所以我们需要先将其 time.localtime(timestamp),再传入strftime
    def format(self, _format="%y-%m-%d %H:%M:%s"):
        return time.strftime(_format, time.localtime(self.timestamp))

    def dur_format(self, _format="%S:%f"):
        __timestamp = int(self.timestamp * 1000)
        res = ""
        i = 0
        n = len(_format)


        while i < n:
            if _format[i] == '%' and i+1<len(_format):
                i+=1
                for it in self.__time_item:
                    if it[0] == _format[i]:
                        res += str(int(__timestamp / it[1]))
                        __timestamp%=it[1]
                        break
            else:
                res += _format[i]
            i += 1

        return res

    def __sub__(self, other):
        return Time(self.timestamp - other.timestamp)

    def __add__(self, other):
        return Time(self.timestamp + other.timestamp)

    def __str__(self):
        return self.format()
    @classmethod
    def now(cls):
        return Time(time.time())

if __name__ == '__main__':
    t1 = Time.now()
    time.sleep(3.45)
    print((Time.now() - t1).dur_format("%M:%S:%u"))
