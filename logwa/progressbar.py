import time

from . import logger
from . import console


class ProgressBar:

    @staticmethod
    def digital_progressbar_func(handling, total, time_start):
        return "{}/{}".format(handling, total)

    @staticmethod
    def percentage_progressbar_func(handling, total, time_start):
        return "{:3}%".format(handling * 100 // total)

    @staticmethod
    def default_progressbar_func(handling, total, time_start):
        percentage = handling * 100 // total
        fin = "■" * percentage
        # 总宽度为102,其中2为符号 -> 的宽度
        nfin = " " * (100 - percentage)

        return "{:3}%[{}->{}] {:.3}s".format(percentage, fin, nfin, time.time() - time_start)

    def __init__(self, total, progressbar_func=None):
        if progressbar_func is None:
            progressbar_func = ProgressBar.default_progressbar_func
        self.progress_func = progressbar_func
        self.total = total
        self.handling = 0
        self.std_logger = logger.Logger(logger.default_config())
        self.logger_list = []
        self.time_start = time.time()
        console.hidden()

    def std_on(self, config):
        self.std_logger = Logger(config)

    def std_off(self):
        self.std_logger = None

    # 此logger只能用于文件输出
    def add_logger(self, config):
        self.logger_list.append(logger.Logger(config))

    def start(self):
        self.time_start = time.time()
        return self

    def __show_bar(self):
        console.write(self.progress_func(self.handling, self.total, self.time_start))
        console.to_linestart()
        console.flush()


    def update(self,count=1):
        self.handling += count
        if self.handling==self.total:
            self.interrupt()



    def debug(self, *args):
        self.debugf("{} "*len(args), *args)


    def debugf(self, msgfmt, *args):
        if self.std_logger != None:
            console.to_linestart()
            console.clear_back()
            self.std_logger.debugf(msgfmt, *args)
            self.__show_bar()
        for l in self.logger_list:
            l.debugf(msgfmt, *args)

    def info(self, *args):
        self.infof("{} "*len(args), *args)

    def infof(self, msgfmt, *args):
        if self.std_logger is not None:
            console.to_linestart()
            console.clear_back()
            self.std_logger.infof(msgfmt, *args)
            self.__show_bar()
        for l in self.logger_list:
            l.infof(msgfmt, *args)

    def warn(self, *args):
        self.warnf("{} "*len(args), *args)

    def warnf(self, msgfmt, *args):
        if self.std_logger != None:
            self.std_logger.warnf(msgfmt, *args)
            self.__show_bar()
        for l in self.logger_list:
            l.warnf(msgfmt, *args)

    def erro(self, *args):
        self.errof("{} "*len(args), *args)

    def errof(self, msgfmt, *args):
        if self.std_logger is not None:
            self.std_logger.errof(msgfmt, *args)
            self.__show_bar()
        for l in self.logger_list:
            l.errof(msgfmt, *args)

    def interrupt(self):
        self.__show_bar()
        console.write("\n")
        console.show()
        console.flush()
        for l in self.logger_list:
            l.target.write(self.progress_func(self.handling, self.total, self.time_start))


if __name__ == '__main__':
    p = ProgressBar(100)
    p.start()
    for i in range(0, 100):
        p.update()
        p.info("okok")
        time.sleep(0.1)
        if i == 50:
            p.interrupt()
            break
