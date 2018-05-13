import jsonrpclib

URL = "http://localhost:6060"

# call backend rpc server 6060, which is different from 4040 which handles getMoreNews()
client = jsonrpclib.ServerProxy(URL)

def classify(text):
    topic = client.classify(text)
    print("Topic: %s" % str(topic))
    return topic