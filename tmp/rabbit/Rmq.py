import pika
import cv2
import zipfile
import json
from datetime import datetime
import base64
import time
import os
import sys


class Rmq:

    def __init__(self, queueName='camlive', ipaddress='62.244.197.146'):
        self.addressIp = ipaddress
        self.queueName = queueName
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(ipaddress, 5550))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queueName)

    def basic_publish(self, data):
        self.channel.basic_publish(exchange='', routing_key=self.queueName, body=data)





