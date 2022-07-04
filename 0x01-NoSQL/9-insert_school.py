#!/usr/bin/env python3
""" Defines insert_school """



def insert_school(mongo_collection, **kwargs):
    """ Inserts a new document in a collection based on kwargs"""
    mongo_collection.insert_many([kwargs])
    return mongo_collection.inserted_ids
