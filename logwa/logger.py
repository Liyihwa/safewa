import sys
from enum import Enum

from safewa.timewa import Time
from .cfmt import cfmt

class Level(Enum):
    debug = 0
    info = 1
    warn = 2
    error = 3


default_datatime_format = "%Y-%m-%d %H:%M:%S"

class Config:
    def __init__(self, use_color, target, level, datatime_format, log_methods, error_raise):
        self.use_color = use_color
        self.target = target
        self.level = level
        self.datatime_format = datatime_format
        self.log_methods = log_methods
        self.error_raise = error_raise


class Logger:
    def __init__(self, config):
        if not isinstance(config, Config):
            raise RuntimeError("The parameter should be an object of Config")
        if config.level.value < Level.debug.value or config.level.value > Level.error.value:
            raise RuntimeError("Config's Level out of range")
        if len(config.log_methods) != 4:
            raise RuntimeError("Log methods error!")
        i = config.level.value
        while i < 4:
            if not callable(config.log_methods[i]):
                raise RuntimeError("Log method [{}]! can't call".format(i))
            i += 1
        self.level = config.level
        self.log_methods = config.log_methods
        self.target = config.target
        self.datatime_format = config.datatime_format
        self.use_color = config.use_color



    def __write(self, level, fmt, method, *args):
        msg = cfmt(self.use_color, fmt, *args)
        res = method(Time.now().format(self.datatime_format), level, msg)
        res = cfmt(self.use_color, res[0], *res[1:])
        self.target.write(res)

    def debugf(self, fmt, *args):
        if self.level.value <= Level.debug.value:
            self.__write("DBUG", fmt, self.log_methods[Level.debug.value], *args)

    def infof(self, fmt, *args):
        if self.level.value <= Level.info.value:
            self.__write("INFO", fmt, self.log_methods[Level.info.value], *args)

    def warnf(self, fmt, *args):
        if self.level.value <= Level.warn.value:
            self.__write("WARN", fmt, self.log_methods[Level.warn.value], *args)

    def errof(self, fmt, *args):
        self.__write("ERRO", fmt, self.log_methods[Level.error.value], *args)
        #msg = cfmt(False, fmt, *args)
        # raise RuntimeError(msg)

    def debug(self, *args):
        self.debugf("{} "*len(args),*args)

    def info(self, *args):
        self.infof("{} "*len(args),*args)

    def warn(self, *args):
        self.warnf("{} "*len(args),*args)

    def erro(self, *args):
        self.errof("{} "*len(args),*args)

    def line(self):
        self.target.write("======================================================\n")


def default_config():
    return Config(True, sys.stdout, Level.info, default_datatime_format, default_methods(), False)


def default_debug(datatime, level, msg):
    return "{} {::g} : {}\n", datatime, level, msg


def default_info(datatime, level, msg):
    return "{} {::u} : {}\n", datatime, level, msg


def default_warn(datatime, level, msg):
    return "{} {::y} : {}\n", datatime, level, msg


def default_erro(datatime, level, msg):
    return "{} {::_rx} : {}\n", datatime, level, msg


def default_methods():
    return default_debug, default_info, default_warn, default_erro


def level_only_debug(datatime, level, msg):
    return "[{::g}] {}\n", level, msg


def level_only_info(datatime, level, msg):
    return "[{::g}] {}\n", level, msg


def level_only_warn(datatime, level, msg):
    return "[{::g}] {}\n", level, msg


def level_only_erro(datatime, level, msg):
    return "[{::g}] {}\n", level, msg


def level_only_methods():
    return level_only_debug, level_only_info, level_only_warn, level_only_erro


def level_only_config():
    return Config(True, sys.stdout, Level.info, default_datatime_format, level_only_methods(), False)


__std = Logger(default_config())


def std_off():
    global __std
    __std = None


def std_on(config):
    global __std
    __std = Logger(config)

def debug( *args):
    if __std is not None:
        __std.debug(*args)

def info(*args):
    if __std is not None:
        __std.info(*args)


def warn( *args):
    if __std is not None:
        __std.warn(*args)

def erro(*args):
    if __std is not None:
        __std.erro(*args)

def debugf(fmt, *args):
    if __std is not None:
        __std.debugf(fmt, *args)

def infof(fmt, *args):
    if __std is not None:
        __std.infof(fmt, *args)

def warnf(fmt, *args):
    if __std is not None:
        __std.warnf(fmt, *args)

def errof(fmt, *args):
    if __std is not None:
        __std.errof(fmt, *args)

def line():
    __std.line()

if __name__ == '__main__':
    config = default_config()
    config.log_methods = level_only_methods()
    std_on(config)
    warn("{::u}", "abc")
    info("{::u}", "abc")
    erro("{::u}", "abc")
    debug("{::u}", "abc")
