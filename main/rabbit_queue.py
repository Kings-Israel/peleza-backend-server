import pika,os


class QueuePublisher:
    def __init__(self):

      print(" [x] Initializing Queue Publisher")


    def sendToqueue (self,requestID): 
        try:
            
            credentials = pika.PlainCredentials('peleza', 'peleza123!') 
            parameters=pika.ConnectionParameters(host='localhost',virtual_host='peleza',port='5672',credentials=credentials,heartbeat=600, blocked_connection_timeout=300) 
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='VerifiedQueue',durable=True)
            channel.basic_publish(exchange='Peleza',
                      routing_key='',
                      body=requestID)
            print(" [x] Sent request to queue") 
            connection.close()          
        except Exception as e:
            print(e)
       
        return