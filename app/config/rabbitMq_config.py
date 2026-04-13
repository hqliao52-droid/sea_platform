# rabbitMQ_config.py

import pika
import json
from app.config.settings import settings


class MQClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MQClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "initialized"):
            return

        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        print("==================",settings.RABBITMQ_HOST, settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)

        self.connection_params = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=5672,
            virtual_host='/',
            credentials=credentials
        )

        self.connection = None
        self.channel = None
        self.initialized = True

        self.queue_name="sea_queue"

    def connect(self):
        if self.connection and not self.connection.is_closed:
            return

        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()

    def publish(self, message: dict):
        self.connect()

        self.channel.queue_declare(queue=self.queue_name, durable=True)

        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
    
    def consume(self):
        self.connect()
        
        # 阻塞式获取单条消息
        method_frame, _, body = self.channel.basic_get(queue=self.queue_name, auto_ack=True)
        
        if method_frame:
            return json.loads(body.decode())
        return None