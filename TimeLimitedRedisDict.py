#!/usr/bin/python3
import json
import redis
import datetime
import time
import statistics

class TimeLimitedRedisDict():
    def __init__(self, redis_key='timelimitedredisdict', redis_object=None, max_length=120):
        self.max_length=max_length
        self.redis_key = redis_key

        if not redis_object:
            self.redis = redis.Redis(host='localhost', port=6379, db=0)
        else:
            self.redis = redis_object

        self.read_dict()

    @staticmethod
    def now():
        return datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S.%f')

    def read_dict(self):
        str_r_val = self.redis.get(self.redis_key)
        if str_r_val:
            self.d = json.loads(str_r_val)
        else:
            self.d = {}

    def write_dict(self):
        self.redis.set(self.redis_key, json.dumps(self.d))

    def __getitem__(self, key):
        self.read_dict()
        return self.d[key]

    def __setitem__(self, key, value):
        self.read_dict()
        kys = sorted(self.d.keys())
        if len(kys) > self.max_length:
            #print("Deleting this key: %s" % kys[0])
            del self.d[kys[0]]

        self.d[key] = value
        self.write_dict()

    def insert(self, value):
        #print(TimeLimitedRedisDict.now())
        self.__setitem__(TimeLimitedRedisDict.now(), value)

    def average(self):
        return self.avg()

    def avg(self):
        self.read_dict()
        try:
            avg = statistics.mean(self.d.values())
        except TypeError:
            raise TypeError("Cannot compute average unless all values in the dict are of similar types")
        return avg

