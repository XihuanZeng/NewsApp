import json
import os
import sys
from bson.json_util import dumps
from utils import mongodb_client
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer


## hello world API
def add(num1, num2):
    print ('add is called with %s and %s' % (num1, num2))
    return num1 + num2

def getOneNews():
    print ('getOneNews is called')
    # random find one
    res = mongodb_client.get_db()['news'].find_one()
    return json.loads(dumps(res))

