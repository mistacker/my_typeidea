import time
from collections import OrderedDict


class LRUCacheDict:
    def __init__(self, max_size=1024, expiration=60):
        """最大容量为1024个key，每个key有效期为60s"""
        self.max_size = max_size
        self.expiration = expiration

        self._cache = {}
        self._access_records = OrderedDict()  # 记录访问时间
        self._expire_records = OrderedDict()  # 记录失效时间

    def __setitem__(self, key, value):
        now = int(time.time())
        self.__delete__(key)

        self._cache[key] = value
        self._expire_records[key] = now + self.expiration
        self._access_records[key] = now

        self.cleanup()

    def __getitem__(self, key):
        result = None
        if key in self._cache:
            now = int(time.time())
            del self._access_records[key]
            self._access_records[key] = now
            self.cleanup()
            result = self._cache.get(key)
        return result

    def __contains__(self, key):
        self.cleanup()
        return key in self._cache

    def __delete__(self, key):
        if key in self._cache:
            del self._cache[key]
            del self._expire_records[key]
            del self._access_records[key]

    def cleanup(self):
        """
            去掉无效(过期或者超出存储大小)的缓存
        """
        if self.expiration is None:
            return None

        pending_delete_keys = []
        now = int(time.time())
        # 删除已经过期的缓存
        for k, v in self._expire_records.items():
            if v < now:
                pending_delete_keys.append(k)

        for del_k in pending_delete_keys:
            self.__delete__(del_k)

        # 如果数据量大于max_size，则删掉最旧的缓存
        while len(self._cache) > self.max_size:
            for k, v in self._access_records.items():
                self.__delete__(k)
                break

    # def get(self, key):
    #     self.__getitem__(key)
    #     return self._cache.get(key)
    #
    # def set(self, key, value):
    #     self.__setitem__(key, value)


if __name__ == '__main__':
    cache_dict = LRUCacheDict(max_size=2, expiration=10)
    cache_dict['name'] = 'python'
    cache_dict['age'] = 30
    cache_dict['addr'] = 'beijing'

    print('name' in cache_dict)
    print('age' in cache_dict)
    print(cache_dict['haha'])
    time.sleep(11)

    print('age' in cache_dict)

# 流程：新建缓存字典，记录初始时间字典，记录过期时间字典他们的key值相同，
#      定义内置删除方法，把字典key值删除，初始时间key值删除，过期时间key值删除
#      定义刷新方法，对超出字典最大数量和过期的数据进行处理
#      定义内置设置方法，把数据写入三个字典中
#      定义内置获取方法，把记录初始时间字典的数据进行刷新
#      定义内置包含方法，判断数据是否存在字典中
