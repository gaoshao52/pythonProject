#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import pika
import commands


def get_ip(dev):
    ip = commands.getoutput("ifconfig %s|sed -n 2p|awk '{print $2}'"%dev)
    return ip

def on_response(ch, method, props, body):
    print(ch, method, props)
    cmd_res = commands.getoutput(str(body))
    # cmd_res = str(body+"wo ai ni")
    print("task isd :", props.reply_to)
    print cmd_res

    ch.queue_declare(queue=props.reply_to)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     body=cmd_res,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id)
                     )

    ch.basic_ack(delivery_tag=method.delivery_tag)




credentials = pika.PlainCredentials('sam', 'sam')
connection = pika.BlockingConnection(pika.ConnectionParameters('10.100.203.154', 5672, '/', credentials))
channel = connection.channel()
channel.exchange_declare(exchange="node_topic", exchange_type="topic")

result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

ip = get_ip("eno1")

# ip = "10.100.203.154"

channel.queue_bind(queue=queue_name,
                   exchange="node_topic",
                   routing_key=ip)

channel.basic_consume(on_response,
                      queue=queue_name)

print("waiting.....")
channel.start_consuming()








