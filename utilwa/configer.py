class Configer:
    def __init__(self, default=None):
        self.__global_default = default
        self.__defaults = {}

    def set_default(self, key, value):
        if key == "":
            self.__global_default = value
        else:
            self.__defaults[key] = value

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        elif item in self.__defaults:
            return self.__defaults[item]
        else:
            return self.__global_default

    def __setattr__(self, key, value):
        self.__dict__[key] = value

