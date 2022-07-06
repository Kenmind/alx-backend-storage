#!/usr/bin/env python3
""" Defines the class Cache """
from functools import wraps
import redis as r
from typing import Any, Callable, Union
import uuid


def count_calls(method: Callable) -> Callable:
    """ Counts calls to a Cache instance"""
    @wraps(method)
    def call(self, *args, **kwargs) -> Any:
        """Counter for count_calls"""
        if isinstance(self._redis, r.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return call


def call_history(method: Callable) -> Callable:
    """Records the call details of a method in Cache """
    @wraps(method)
    def history(self, *args) -> Any:
        """Prints the output of a method after storing the inputs and output.
        """
        k_in = '{}:inputs'.format(method.__qualname__)
        k_out = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, r.Redis):
            self._redis.lpush(k_in, str(args))
        output = method(self, *args)
        if isinstance(self._redis, r.Redis):
            self._redis.lpush(k_out, output)
        return output
    return history


class Cache:
    """Cache class"""
    def __init__(self) -> None:
        """ Initializes cache"""
        self._redis = r.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
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
