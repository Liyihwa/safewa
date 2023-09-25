import copy


class Map:
    def __init__(self, dic):
        self.dic = {}
        dic = copy.deepcopy(dic)
        for k, v in dic.items():
            if isinstance(v, dict):
                self.dic[k] = Map(v)
            else:
                self.dic[k] = v

    @staticmethod
    def from_dict(dic):
        return Map(dic)

    def __str__(self):
        return str(self.to_dict())



    def __to_dict(self):
        dic = {}
        for k, v in self.dic.items():
            if isinstance(v, Map):
                dic[k] = v.to_dict()
            else:
                dic[k] = v
        return dic

    def to_dict(self):
        return copy.deepcopy(self).__to_dict()

    def set(self, key, val):
        self.dic[key] = val
        return self

    def __setitem__(self, key, value):
        self.set(key, value)

    def get(self, key):
        return self.dic[key]

    def __getitem__(self, item):
        return self.get(item)

    def contains(self, key):
        return key in self.dic

    def clone(self):
        return copy.deepcopy(self)
