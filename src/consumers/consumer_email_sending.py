from typing import Sequence
from dataclasses import dataclass
from start import app
from server.amqp import AMQPConsumer


@dataclass
class ConsumerEmailSendingPayload:
    to: Sequence[str]
    title: str
    message: str


@app.amqp.add_consumer(
    "consumer_email_sending",
    "queue_email_sending",
    ack=True,
    data_class=ConsumerEmailSendingPayload,
)
class ConsumerEmailSending(AMQPConsumer):
    def on_message_queue(self, body: ConsumerEmailSendingPayload, **kwargs) -> None:
        app.smtp.send(body.to, body.title, body.message)
