import os
import json
import logging
import random
import argparse
from datetime import datetime
from typing import Dict, NamedTuple

from kafka import KafkaProducer
from kafka.errors import KafkaError


USERNAME = os.environ.get("KAFKA_USERNAME")
PASSWORD = os.environ.get("KAFKA_PASSWORD")
CA_CERTIFICATE_PATH = os.path.join(
    ".env/ca-certificates/Yandex/YandexInternalRootCA.crt"
)
DEFAULT_SERVERS = [
    "rc1a-6d6fp6492vk5vrni.mdb.yandexcloud.net:9091",
    "rc1b-u5c48h5qgira5176.mdb.yandexcloud.net:9091",
    "rc1d-e2uh1h9iltff3lm1.mdb.yandexcloud.net:9091",
]


class RecordMetadata(NamedTuple):
    topic: str
    partition: int
    offset: int


def main():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        "-t", "--topic", default="clicks", help="kafka topic to consume"
    )
    argparser.add_argument(
        "-n",
        default=10,
        type=int,
        help="number of messages to send",
    )

    args = argparser.parse_args()

    producer = KafkaProducer(
        bootstrap_servers=DEFAULT_SERVERS,
        security_protocol="SASL_SSL",
        sasl_mechanism="SCRAM-SHA-512",
        sasl_plain_username=USERNAME,
        sasl_plain_password=PASSWORD,
        ssl_cafile=CA_CERTIFICATE_PATH,
        value_serializer=serialize,
    )

    try:
        for _ in range(args.n):
            record_md = send_message(producer, args.topic)
            print(
                f"Msg sent. Topic: {record_md.topic}, partition:{record_md.partition}, offset:{record_md.offset}"
            )
    except KafkaError as err:
        logging.exception(err)

    # Когда вызывается flush, KafkaProducer блокируется и ждет,
    # пока все буферизованные записи будут отправлены и подтверждены брокером Kafka.
    # Это особенно важно, когда вы хотите быть уверены, что все сообщения были успешно доставлены 
    # перед тем, как закрыть продюсера или завершить программу.
    producer.flush()
    producer.close()


def send_message(producer: KafkaProducer, topic: str) -> RecordMetadata:
    click = generate_click()
    future = producer.send(
        topic=topic,
        key=str(click["page_id"]).encode("ascii"),
        value=click,
    )

    # Block for 'synchronous' sends
    record_metadata = future.get(timeout=1)

    return RecordMetadata(
        topic=record_metadata.topic,
        partition=record_metadata.partition,
        offset=record_metadata.offset,
    )


def generate_click() -> Dict:
    return {
        "ts": datetime.now().isoformat(),
        "user_id": random.randint(0, 100),
        "page_id": random.randint(0, 10),
    }


def serialize(msg: Dict) -> bytes:
    return json.dumps(msg).encode("utf-8")


if __name__ == "__main__":
    main()
