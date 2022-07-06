#!/usr/bin/env python3
""" Defines the class Cache """
import redis as r
from typing import Callable, Union
import uuid


class Cache:
    """Cache class"""
    def __init__(self) -> None:
        """ Initializes cache"""
        self._redis = r.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[bytes, float, int, str]) -> str:
        """Stores data in redis and returns the key"""
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[bytes,
                                                          float, int, str]:
        """ Converts data back to the desired format """
        d_key = self._redis.get(key)
        if fn is not None:
            return fn(d_key)
        else:
            return d_key

    def get_str(self, key: str) -> str:
        """ Converts data to string """
        return self.get(key, lambda x: str(x))

    def get_int(self, key: str) -> int:
        """ Converts data to int """
        return self.get(key, lambda x: int(x))
