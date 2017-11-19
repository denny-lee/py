#!/usr/bin/env python
# _*_ coding: utf-8
import pika
credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.104',5672,'/base',credentials))
channel = connection.channel()
# channel.queue_declare(queue='hello')
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
channel.start_consuming()