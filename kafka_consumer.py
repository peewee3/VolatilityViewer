import argparse
import os
import socket
from dotenv import load_dotenv

from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer


class call_option(object):
    def __init__(self, contractSymbol, strikePrice, lastPrice, timeTillExpiry, optionType, pricePerUnit, currentPrice):
        self.contractSymbol = contractSymbol
        self.strikePrice = strikePrice
        self.lastPrice = lastPrice
        self.timeTillExpiry = timeTillExpiry
        self.optionType = optionType
        self.pricePerUnit = pricePerUnit
        self.currentPrice = currentPrice

def dict_to_call(obj, ctx):
    if obj is None:
        return None
    # Need to include the contract symbol key here somehow
    return call_option(strikePrice=obj['StrikePrice'],
                contractSymbol=obj['ContractSymbol'],
                lastPrice=obj['LastPrice'],
                timeTillExpiry=obj['TimeTillExpiry'],
                optionType=obj["OptionType"],
                pricePerUnit=obj["PricePerUnit"],
                currentPrice=obj["CurrentPrice"])

def main():
    topic = "Yahoo_Finance"
    load_dotenv()

    schema_registry_conf = {
    "url": os.getenv("KAFKA_SCHEMA_REGISTRY_URL"),
    "basic.auth.user.info": f'{os.getenv("KAFKA_SCHEMA_REGISTRY_API_KEY")}:{os.getenv("KAFKA_SCHEMA_REGSITRY_SECRET")}'
    }

    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    subject_name = "Yahoo_Finance_Calls"
    schema = schema_registry_client.get_latest_version(subject_name)

    avro_deserializer = AvroDeserializer(schema_registry_client,
                                         schema.schema.schema_str,
                                         dict_to_call)

    conf = {'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVER'),
            'security.protocol': 'SASL_SSL',
            'sasl.mechanism': 'PLAIN',
            'sasl.username': os.getenv('KAFKA_API_KEY'),
            'sasl.password': os.getenv('KAFKA_API_SECRET'),
            'client.id': socket.gethostname(),
            'group.id': 1,
            'auto.offset.reset': "earliest"
            }

    consumer = Consumer(conf)
    consumer.subscribe([topic])

    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            call_option = avro_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
            if call_option is not None:
                print(call_option.contractSymbol)
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == '__main__':
    main()