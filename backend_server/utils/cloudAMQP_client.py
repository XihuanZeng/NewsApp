import pika

## here we need multiple connection, cannot use singleton
class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameter(cloud_amqp_url)
        self.params.socket_timeout = 3

        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue = queue_name)

    def sendMessage(self, message):
        ## exchange we use default
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(message))
        print("[x] Sent message to %s:%s" % (self.queue_name, message))

    # get only one message
    def getMessage(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        ## only when there is message in queue, here evaluate as True
        if method_frame:
            print("[x] Sent message to %s:%s" % (self.queue_name, body))
            # acknowledge, need to tell the queue I receive the message
            # must have this tag so that queue know it is this msg get 
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body.decode('utf-8'))
        else:
            print ('No message returned')
            return None

    # AMQP has a sleep, i.e heartbeat
    def sleep(self, seconds):
        # pika function, keep heartbeat while sleep.
        # note if you use Thread.sleep() your heartbeat sleep as well
        self.connection.sleep()
        

