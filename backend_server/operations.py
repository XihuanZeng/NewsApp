import json
import os
import sys
from bson.json_util import dumps
import mongo_client
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

sys.path.append(ps.path.dir_name(__file__), 'utils')

## hello world API
def add(num1, num2):
    print ('add is called with %s and %s' % (num1, num2))
    return num1 + num2

def getOneNews():
    print ('getOneNews is called')
    # random find one
    res = mongo_client.get_db()['news'].find_one()
    return json.load(dump(res))

