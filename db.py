import pymongo

def insert(json, table):
    table.insert_one(json)