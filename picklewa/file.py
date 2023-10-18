import pickle

from .. import oswa

# 一次读取多个对象
def load_all(filepath):
    if not oswa.isfile(filepath):
        raise FileNotFoundError
    pickles = []
    with open(filepath, 'rb') as f:
        while True:
            try:
                obj = pickle.load(f)
                # 处理读取到的对象
                pickles.append(obj)
            except EOFError:
                break
    return pickles


def dump_all(filepath, *datas):
    with open(filepath, 'wb') as f:
        for data in datas:
            pickle.dump(data, f)
