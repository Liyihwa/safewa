import sys
from enum import Enum
import cfmt
from timewa import Time

class Level(Enum):
    debug = 0
    info = 1
    warn = 2
    error = 3


default_datatime_format = "06-01-02 15:04:05.000"


class Config:
    def __init__(self, use_color, target, level, datatime_format, log_methods):
        self.use_color = use_color
        self.target = target
        self.level = level
        self.datatime_format = datatime_format
        self.log_methods = log_methods


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
            i+=1
        self.level = config.level
        self.log_methods = config.log_methods
        self.target = config.target
        self.datatime_format = config.datatime_format
        self.use_color = config.use_color

    def write(self, level, fmt, method, *args):
        msg = cfmt.cfmt(self.use_color, fmt, *args)
        res = method(Time.now().format(self.datatime_format), level, msg)
        res = cfmt.cfmt(self.use_color, res[0], * res[1:])
        self.target.write(res)

    def debug(self, fmt, *args):
        if self.level.value <= Level.debug.value:
            self.write("DEBUG", fmt, self.log_methods[Level.debug.value], *args)

    def info(self, fmt, *args):
        if self.level.value <= Level.info.value:
            self.write("INFO", fmt, self.log_methods[Level.info.value], *args)

    def warn(self, fmt, *args):
        if self.level.value <= Level.warn.value:
            self.write("WARN", fmt, self.log_methods[Level.warn.value], *args)

    def erro(self, fmt, *args):
        self.write("ERRO", fmt, self.log_methods[Level.error.value], *args)
        msg = cfmt.cfmt(False, fmt, *args)
        raise RuntimeError(msg)


def default_config():
    return Config(True, sys.stdout, Level.info, default_datatime_format, default_methods())


def default_debug(datatime, level, msg):
    return "{} {<5:g} : {}\n", datatime, level, msg


def default_info(datatime, level, msg):
    return "{} {<5:u} : {}\n", datatime, level, msg


def default_warn(datatime, level, msg):
    return "{} {<5:y} : {}\n", datatime, level, msg


def default_erro(datatime, level, msg):
    return "{} {<5:_rx} : {}\n", datatime, level, msg


def default_methods():
    return default_debug, default_info, default_warn, default_erro


def level_only_debug(datatime, level, msg):
    return "[{-5:g}] {}\n", level, msg


def level_only_info(datatime, level, msg):
    return "[{-5:g}] {}\n", level, msg


def level_only_warn(datatime, level, msg):
    return "[{-5:g}] {}\n", level, msg


def level_only_erro(datatime, level, msg):
    return "[{-5:g}] {}\n", level, msg


def level_only_methods():
    return level_only_debug, level_only_info, level_only_warn, level_only_erro


std = Logger(default_config())


def std_off():
    global std
    std = None


def std_on(config):
    global std
    std = Logger(config)


def debug(fmt, *args):
    if std is not None:
        std.debug(fmt, *args)


def info(fmt, *args):
    if std is not None:
        std.info(fmt, *args)


def warn(fmt, *args):
    if std is not None:
        std.warn(fmt, *args)


def erro(fmt, *args):
    if std is not None:
        std.erro(fmt, *args)


if __name__=='__main__':
    print(cfmt.cfmt(True,""))
    config=default_config()
    config.log_methods=level_only_methods()
    warn("{:u}","abc")
    info("{:u}","abc")
    erro("{:u}","abc")
    debug("{:u}","abc")

