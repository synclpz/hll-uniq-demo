import json
import time
import logging as log
from random import randint
from string import ascii_letters

from kafka import KafkaProducer

if __name__ == "__main__":
    log.basicConfig(format="%(asctime)s %(levelname)s"
                    " [%(module)s/%(funcName)s]"
                    " (%(processName)s) %(message)s",
                    level=log.INFO)
    size = 10
    message_count = 10000
    days_count = 100
    bootstrap_servers = "localhost:9092"
    topic_name = "requests"

    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    [
        producer.send(
            topic_name, {
                "timestamp":
                int(time.time() + 86400 * i),
                "cookie":
                "".join([
                    ascii_letters[randint(0,
                                          len(ascii_letters) - 1)]
                    for n in range(size)
                ])
            }) for i in range(days_count) for _ in range(message_count)
    ]
    producer.close()
    log.info("Done")
