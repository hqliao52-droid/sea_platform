import json
import aio_pika
import asyncio

from aio_pika import Message, connect_robust

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

        self.connection = None
        self.channel = None
        self.queue_name = settings.RABBITMQ_NAME
        self.initialized = True

    # connect
    async def connect(self):
        if self.connection and not self.connection.is_closed:
            return

        self.connection = await connect_robust(
            host=settings.RABBITMQ_HOST or "localhost",
            port=settings.RABBITMQ_PORT or 5672,
            login=settings.RABBITMQ_DEFAULT_USER,
            password=settings.RABBITMQ_DEFAULT_PASSWORD,
            virtual_host="/",
            heartbeat=600
        )
        self.channel = await self.connection.channel()

        #  限制消费速度
        await self.channel.set_qos(prefetch_count=3)

        await self.channel.declare_queue(self.queue_name, durable=True)

    # publish
    async def publish(self, message: dict):
        if self.channel is None or self.channel.is_closed:
            await self.connect()

        body = json.dumps(message, ensure_ascii=False).encode()
        # 消息持久化
        msg = Message(body,delivery_mode=aio_pika.DeliveryMode.PERSISTENT)

        await self.channel.default_exchange.publish(msg, routing_key=self.queue_name)

    # consume
    async def consume(self, callback):
        """
        异步推模式消息
        """
        if self.channel is None or self.channel.is_closed:
            await self.connect()

        queue = await self.channel.declare_queue(self.queue_name, durable=True)

        async def _handler(message: aio_pika.IncomingMessage):
            async with message.process(requeue_on_error=True):
                try:
                    body = message.body.decode()
                    msg_dict = json.loads(body)
                    await callback(msg_dict)
                except Exception as e:
                    print(f"Error processing message: {e}")
                    # 重新入队
                    raise

        await queue.consume(_handler)
        print("MQ consumer started...")

        try:
            await asyncio.Future()
        except Exception as e:
            print(f"Error closing connection: {e}")
            await self.connection.close()