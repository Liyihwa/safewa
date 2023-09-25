import configparser


class Configer:
    def __init__(self,filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    @staticmethod
    def build(filename):
        return Configer(filename)

    def get(self,type,section,key,default=None):
        res=None
        if not self.config.has_option(section,key):
            if default is None:
                raise Exception("No option {}:{}".format(section,key))
            else:
                res=default
        else:
            res=self.config.get(section,key)

        if type==bool:
            if res.lower()=="false":
                return False
            elif res.lower()=="true":
                return True
            else:
                raise Exception("Unknown bool value {}".format(res))
        return type(res)


