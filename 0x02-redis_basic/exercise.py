#!/usr/bin/env python3
""" Defines the class Cache """
import redis as r
from typing import Union
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
