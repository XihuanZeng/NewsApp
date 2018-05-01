import operations
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer


SERVER_HOST = 'localhost'
SERVER_PORT = 4040


## hello world API
def add(num1, num2):
    print ('add is called with %s and %s' % (num1, num2))
    return operations.add(num1, num2)

def get_one_news():
    print ('getOneNews is called')
    # random find one
    return  operations.getOneNews()

def get_news_summaries_for_user(user_id, page_number):
    """
    summaries means there is no news content back
    """
    print ("get news summaries for user is called with %s and %s" % (user_id, page_number))
    return operations.getNewsSummariesForUser(user, page_number)



RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
## 'add' is what exposed to external user 
RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(get_one_news, 'get_one_news')
RPC_SERVER.register_function(get_news_summaries_for_user, 'get_news_summaries_for_user')

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