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

        credentials = pika.PlainCredentials(
            settings.RABBITMQ_DEFAULT_USER,
            settings.RABBITMQ_DEFAULT_PASSWORD
        )

        self.connection_params = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=5672,
            virtual_host='/',
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )

        self.connection = None
        self.channel = None
        self.initialized = True
        self.queue_name = "sea_queue"

    # =========================
    # connect
    # =========================
    def connect(self):
        if self.connection and self.connection.is_open:
            return

        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()

        # ⭐⭐⭐ 核心优化：限制消费速度（解决 worker 吃爆）
        self.channel.basic_qos(prefetch_count=3)

        self.channel.queue_declare(
            queue=self.queue_name,
            durable=True
        )

    # =========================
    # publish（保留）
    # =========================
    def publish(self, message: dict):
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()
        channel.queue_declare(
            queue=self.queue_name,
            durable=True
        )
        channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message,ensure_ascii=False),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
        channel.close()
        connection.close()

    # =========================
    # consume（🔥关键修改）
    # =========================
    def consume(self, callback):
        """
        ✔ 改成推模式消费
        ✔ 支持 qos
        ✔ 不再轮询
        """
        self.connect()

        def _handler(ch, method, properties, body):
            message = json.loads(body.decode())
            callback(ch,method,message)

            # ⭐ 手动 ack（非常重要）
            # ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=_handler,
            auto_ack=False
        )

        print("MQ consumer started...")
        self.channel.start_consuming()