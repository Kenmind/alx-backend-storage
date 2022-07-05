#!/usr/bin/env python3
""" Provides stats about Nginx logs restored in mongoDB"""
import pymongo as pm
import pprint

db = pm.MongoClient()
mydb = db["logs"]
mycol = mydb["nginx"]


get_get = mycol.count_documents({"method": "GET"})
get_post = mycol.count_documents({"method": "POST"})
get_put = mycol.count_documents({"methods": "PUT"})
get_patch = mycol.count_documents({"method": "PATCH"})
get_delete = mycol.count_documents({"method": "DELETE"})
get_total = mycol.count_documents({})
get_status = mycol.count_documents({"method": "GET", "path": "/status"})
get_all = mycol.find({})


print("{} logs".format(get_total))
print("Methods:\n\tmethod GET: {}\n\tmethod POST: {}\n\tmethod PUT\
: {}\n\tmethod PATCH: {}\n\tmethod DELETE: {}\n{} status \
check".format(get_get, get_post, get_put,
              get_patch, get_delete, get_status))
print("IPs:\n\t{}".format(get_all))
pprint(get_all)
