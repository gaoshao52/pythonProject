#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pika
import random
import re

class Client(object):
    def __init__(self):
        self.host_ip= []
        self.cmd = ""
        credentials = pika.PlainCredentials('sam', 'sam')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('10.100.203.154', 5672, '/', credentials))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange="node_topic", exchange_type="topic")


    def send_message(self):
        task_id = str(random.randrange(1000, 2000))
        print("task id: %s"%task_id)
        # print("cmd", self.cmd)
        for routing_key in self.host_ip:
            # print("ip", routing_key)
            self.channel.basic_publish(exchange='node_topic',
                                       routing_key=routing_key,
                                       body=self.cmd,
                                       properties=pika.BasicProperties(
                                           reply_to=task_id,
                                           correlation_id=routing_key
                                            )
                                       )


    def get_result(self, task_id):

        self.channel.queue_declare(queue=task_id)

        self.channel.basic_consume(self.handle_response,
                                   queue=task_id)

        for i in range(len(self.host_ip)):
            self.connection.process_data_events()


    def handle_response(self, ch, method, props, body):
        print("Recv: %s, %s"%(props.correlation_id, body))

        ch.basic_ack(delivery_tag=method.delivery_tag)


    def interactive(self):
        while True:
            user_str = raw_input(">>:").strip()
            if user_str.startswith("run"):
                if re.match("run.+--hosts.+", user_str) is None:
                    continue
                self.cmd = re.search("\".+\"", user_str).group().strip("\"")

                self.host_ip = re.findall("\d+\.\d+\.\d+\.\d+", user_str)
                # print("host_ip", self.host_ip)
                self.send_message()
                continue
            elif user_str.startswith("check_task"):
                task_id = re.search("\d+", user_str).group()
                self.get_result(task_id)

            else:
                continue





if __name__ == '__main__':
    # mingling = 'run "df -h" --hosts 192.168.3.55 10.4.3.4'
    # print(re.match("run.+--hosts.+", mingling))
    # print(re.search("\".+\"", mingling).group().strip("\""))
    # print(re.findall("\d+\.\d+\.\d+\.\d+", mingling))
    Client().interactive()













