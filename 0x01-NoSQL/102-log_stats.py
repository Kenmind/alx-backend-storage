#!/usr/bin/env python3
""" Provides stats about Nginx logs restored in mongoDB """
from pymongo import MongoClient"""import pymongo as pm
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

IPs = mycol.aggregate([{
    "$group": {
        "_id": "$ip", "count": {"$sum": 1}
        }}, {"$sort": {"count": -1}}, {"$limit": 10}, {"$project": {
            "_id": 0, "ip": "$_id", "count": 1}}
])

print("{} logs".format(get_total))
print("Methods:\n\tmethod GET: {}\n\tmethod POST: {}\n\tmethod PUT\
: {}\n\tmethod PATCH: {}\n\tmethod DELETE: {}\n{} status \
check".format(get_get, get_post, get_put,
              get_patch, get_delete, get_status))
print("IPs:")
for top in IPs:
    count = top.get("count")
    ip_address = top.get("ip")
    print("\t{}: {}".format(ip_address, count))

def nothing():
   """" Does nothing""""
    pass

def do_not():
    """" Do nothing as well """"
    pass"""


def print_nginx_request_logs(nginx_collection):
    '''Prints stats about Nginx request logs.
    '''
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = len(list(nginx_collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, req_count))
    status_checks_count = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(status_checks_count))


def print_top_ips(server_collection):
    '''Prints statistics about the top 10 HTTP IPs in a collection.
    '''
    print('IPs:')
    request_logs = server_collection.aggregate(
        [
            {
                '$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}
            },
            {
                '$sort': {'totalRequests': -1}
            },
            {
                '$limit': 10
            },
        ]
    )
    for request_log in request_logs:
        ip = request_log['_id']
        ip_requests_count = request_log['totalRequests']
        print('\t{}: {}'.format(ip, ip_requests_count))


def run():
    '''Provides some stats about Nginx logs stored in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)
    print_top_ips(client.logs.nginx)


if __name__ == '__main__':
    run()
