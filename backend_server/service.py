import operations
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

sys.path.append(ps.path.dir_name(__file__), 'utils')

## hello world API
def add(num1, num2):
    print ('add is called with %s and %s' % (num1, num2))
    return num1 + num2

def getOneNews():
    print ('getOneNews is called')
    # random find one
    return  operations.getOneNews()


RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
## 'add' is what exposed to external user 
RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(getOneNews, 'getOneNews')

print ("Starging RPC on %s:%s" % (SERVER_HOST, SERVER_PORT))
RPC_SERVER.serve_forever()

