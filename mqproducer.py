#!/usr/bin/env python
# _*_ coding: utf-8
import pika
credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.104',5672,'/base',credentials))
channel = connection.channel()
channel.queue_declare(queue='hello',durable=True)
channel.basic_publish(exchange='',
                  routing_key='hello',
                  body='Hello World!',
                    properties=pika.BasicProperties(
                          delivery_mode=2
                      )
                      )
print("开始队列")
connection.close()