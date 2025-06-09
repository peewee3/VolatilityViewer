from confluent_kafka import Producer
from dotenv import load_dotenv
import socket
import pandas
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
import os


class call_option(object):
    def __init__(self, contractSymbol, strikePrice, lastPrice, timeTillExpiry, optionType, pricePerUnit, currentPrice):
        self.contractSymbol = contractSymbol
        self.strikePrice = strikePrice
        self.lastPrice = lastPrice
        self.timeTillExpiry = timeTillExpiry
        self.optionType = optionType
        self.pricePerUnit = pricePerUnit
        self.currentPrice = currentPrice

def call_to_dict(call_option, ctx):
    return dict(StrikePrice = call_option.strikePrice,
                LastPrice = call_option.lastPrice,
                TimeTillExpiry = call_option.timeTillExpiry,
                OptionType = call_option.optionType,
                PricePerUnit = call_option.pricePerUnit,
                CurrentPrice = call_option.currentPrice)

def delivery_report(err, msg):
    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


def main():
    load_dotenv()

    conf = {'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVER'),
            'security.protocol': 'SASL_SSL',
            'sasl.mechanism': 'PLAIN',
            'sasl.username': os.getenv('KAFKA_API_KEY'),
            'sasl.password': os.getenv('KAFKA_API_SECRET'),
            'client.id': socket.gethostname(),
            }

    schema_registry_conf = {
        "url": os.getenv("KAFKA_SCHEMA_REGISTRY_URL"),
        "basic.auth.user.info": f'{os.getenv("KAFKA_SCHEMA_REGISTRY_API_KEY")}:{os.getenv("KAFKA_SCHEMA_REGSITRY_SECRET")}'
    }

    
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    subject_name = "Yahoo_Finance_Calls"
    schema = schema_registry_client.get_latest_version(subject_name)
    
    avro_serializer = AvroSerializer(
                            schema_registry_client,
                            schema.schema.schema_str,
                            call_to_dict)
    
    string_serializer = StringSerializer('utf_8')


    calls_df = pandas.read_csv("/Users/petermaher/Desktop/Yahoo Finance/calls.csv")
    

    producer = Producer(conf)
    topic = "Yahoo_Finance"

    producer.poll(0.0)
    for _, row in calls_df.iterrows():
        producer.poll(0.0)
        try:
            contractSymbol = row["Contract Symbol"]
            strikePrice = row["Strike Price"]
            lastPrice = row["Last Price"]
            timeTillExpiry = row["Time till expiry"]
            optionType = row["Option Type"]
            pricePerUnit = row["Price Per Unit"]
            currentPrice = row["Current Price"]

            option = call_option(contractSymbol,
                                    strikePrice,
                                    lastPrice,
                                    timeTillExpiry,
                                    optionType,
                                    pricePerUnit,
                                    currentPrice)
            
            producer.produce(topic=topic,
                            key=string_serializer(str(option.contractSymbol)),
                            value=avro_serializer(option, SerializationContext(topic, MessageField.VALUE)),
                            on_delivery=delivery_report)
            
        except KeyboardInterrupt:
            break
        except ValueError:
            print("Invalid input, discarding record...")
            continue

    print("\nFlushing records...")
    producer.flush()

if __name__ == "__main__":
    main()


