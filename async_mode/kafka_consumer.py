import os
import json
import argparse

from kafka import KafkaConsumer


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


def main():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        "-g", "--group_id", required=True, help="kafka consumer group_id"
    )
    argparser.add_argument(
        "-t", "--topic", default="clicks", help="kafka topic to consume"
    )

    args = argparser.parse_args()

    consumer = KafkaConsumer(
        bootstrap_servers=DEFAULT_SERVERS,
        security_protocol="SASL_SSL",
        sasl_mechanism="SCRAM-SHA-512",
        sasl_plain_username=USERNAME,
        sasl_plain_password=PASSWORD,
        ssl_cafile=CA_CERTIFICATE_PATH,
        group_id=args.group_id,
        value_deserializer=json.loads,
    )

    consumer.subscribe(topics=[args.topic])

    model_inference(consumer)


def model_inference(consumer):
    count = 0
    print("Waiting for a new messages. Press Ctrl+C to stop")
    try:
        for msg in consumer:
            print(
                f"{msg.topic}:{msg.partition}:{msg.offset}: key={msg.key} value={msg.value}"
            )
            count += 1
    except KeyboardInterrupt:
        pass
    print(f"Total {count} messages received")


if __name__ == "__main__":
    main()
