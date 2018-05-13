import operations
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer


SERVER_HOST = 'localhost'
SERVER_PORT = 4040


## hello world API
def add(num1, num2):
    print ('add is called with %s and %s' % (num1, num2))
    return operations.add(num1, num2)

def getOneNews():
    """ Test method to get one news """
    print("getOneNews is called")
    return operations.getOneNews()

def getNewsSummariesForUser(user_id, page_num):
    """ Get news summaries for a user """
    print("getNewsSummariesForUser is called with %s and %s" % (user_id, page_num))
    return operations.getNewsSummariesForUser(user_id, page_num)

def logNewsClickForUser(user_id, news_id):
    print("logNewsClickForUser is called with %s and %s" % (user_id, news_id))
    return operations.logNewsClickForUser(user_id, news_id)

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
## 'add' is what exposed to external user 
RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(getOneNews, 'getOneNews')
RPC_SERVER.register_function(getNewsSummariesForUser, 'getNewsSummariesForUser')
RPC_SERVER.register_function(logNewsClickForUser, 'logNewsClickForUser')

print ("Starting RPC on %s:%s" % (SERVER_HOST, SERVER_PORT))
RPC_SERVER.serve_forever()

"""
to test it, use Postman
POST localhost:3000

body: application/json
{
	"jsonrpc": 2.0,
	"id":123,
	"method":"add",
	"params":[4,5]
}

Note that "jsonrpc":2.0 can be think of default,
this will be recognized by SimpleJSONRPCServer
"""