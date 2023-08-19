#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020-2022 by ZHANG ZHIJIE.
# All rights reserved.

# Created Time: 2023-08-12 09:48
# Author: ZHANG ZHIJIE
# Email: norvyn@norvyn.com
# Git: @n0rvyn
# File Name: conn_mongo.py
# Tools: PyCharm

"""
--- Connecting to MongoDB and operating data ---
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from inspect import currentframe, getframeinfo


class MongoDB(object):
    def __init__(self, server: str = None, port: int = 27017,
                 username: str = None, password: str = None,
                 uri: str = None,
                 server_api=ServerApi('1'),
                 database: str = None,
                 collection: str = None):

        server = 'localhost' if not server and not uri else server
        database = 'dupli_clean_db' if not database else database
        collection = 'dupli_clean_coll' if not collection else collection

        if uri:
            self.client = MongoClient(uri, server_api=server_api)
        else:
            self.client = MongoClient(host=server, port=port,
                                      username=username, password=password,
                                      server_api=server_api)

        self.collection = self.client[database][collection]
        # BSON type Date
        # datetime.today().replace(microsecond=0)

    def reset_collection(self):
        return self.collection.drop()

    def insert_dict(self, data: dict, insert_even_exist: bool = False):
        search_data_in_mongo = list(self.collection.find(data))
        no_data_before = len(search_data_in_mongo)

        # 'DO NOT INSERT IF EXIST' enabled, and data exist, just return the '_id' of structure.
        if not insert_even_exist and no_data_before:
            try:
                data_in_mongo_id = search_data_in_mongo[0]['_id']
            except IndexError:
                raise 'Search MongoDB failed, file: mongodb.py, line: 53.'
            except KeyError:
                raise 'Search MongoDB failed, file: mongodb.py, line: 55.'

            return data_in_mongo_id

        self.collection.insert_one(data)  # after inserted to MongoDB, data will be added a key '_id'
        data_in_mongo_id = data['_id']
        try:
            data.pop('_id')
        except KeyError:
            pass

        no_data_after = len(list(self.collection.find(data)))
        # return True if no_data_after > no_data_before else False
        # return MongoDB '_id' for further use.
        return data_in_mongo_id if no_data_after > no_data_before else None

    def insert_list(self, data: list, insert_even_exist: bool = False):
        """
        Inserting a list of dict, like [{'name': 'John'}, {'name': 'Jack'}]

        return: (the_length_of_data_to_insert, the_ids_in_mongodb_after_inserted)
        """
        no_to_insert = len(data)
        no_before_insert = self.collection.count_documents({})

        # inserting data to MongoDB collection
        result = self.collection.insert_many(data)

        ids = result.inserted_ids
        no_after_insert = self.collection.count_documents({})

        return (no_to_insert, ids) if no_after_insert - no_before_insert == no_to_insert else (0, None)

    def find_by_array_size(self, key: str, size: int):
        _filter = {key: {'$size': {'$gt': 1}}}
        """
        db.inventory.find({tags:{$where:'this.tags.length >= 1'}}
        """
        _filter = {'tags': {"$where": 'this.tags.length > 1'}}
        result = self.collection.find(_filter)

        # result = list(result)
        return result

    def update_value(self, lookup_key: str, lookup_value: str,
                     update_key: str, to_value: str,
                     fresh_m_time: bool = True,
                     update_all: bool = False):
        """
        If 'lookup_key' equals 'update_key', just modify the value of key 'lookup_key'.
        If 'update_key' is different to 'lookup_kdy', adding a new record.
        """
        _filter = {lookup_key: lookup_value}
        _updater = {"$set": {update_key: to_value}, "$currentDate": {"lastModified": True if fresh_m_time else False}}
        _verifier = {lookup_key: lookup_value, update_key: to_value}
        # return self.client[database][collection].find_one_and_update(_filter, _updater)
        self.collection.update_one(_filter, _updater) if not update_all else self.collection.update_many(_filter, _updater)
        return True if self.collection.find_one(_verifier) else False


if __name__ == '__main__':
    mongo = MongoDB()
    print(mongo.find_by_array_size('5bf75e8f5a9be1b18faddb67c40fe8d0', 1))

