from gzip import GzipFile
from io import BytesIO
import zmq
import zmq.asyncio
from asyncio_paho import AsyncioPahoClient
from lxml import etree

from config import *


def async_process(msg, name, config=None):
    address = msg[0].decode('utf-8')
    contents = b"".join(msg[1:])

    message = GzipFile('', 'r', 0, BytesIO(contents)).read()
    topic = name + "/" + address.lstrip('/')

    messages_out = [(topic, message, False)]
    if config is not None and address in config:
        topic_config = config[address]
        tree = etree.parse(BytesIO(message))
        output = []
        for path in topic_config['paths']:
            value = tree.xpath(path, namespaces=topic_config['namespaces'])
            if len(value) == 1:
                output.append(value[0].text)
        new_topic = (topic_config['topic_prefix'] + "/".join(output)).lower()
        messages_out.append((new_topic, message, True))
    return messages_out



async def recv_and_process(ctx, port, name, config=None):
    sock = ctx.socket(zmq.SUB)
    url = "tcp://pubsub.besteffort.ndovloket.nl:%s" % (port,)
    clientid = "feeder-%s" % (name,)
    print("Connecting to %s as %s" % (url, clientid))
    sock.connect(url)
    sock.setsockopt_string(zmq.SUBSCRIBE, "/")

    mqtt = AsyncioPahoClient(client_id=clientid)
    mqtt.username_pw_set(MQTT_USER, password=MQTT_PASSWORD)
    await mqtt.asyncio_connect(MQTT_HOST, MQTT_PORT)

    while True:
        msg = await sock.recv_multipart()  # waits for msg to be ready
        parsed = async_process(msg, name, config)  # We can return multiple messages
        for (topic, payload, retain) in parsed:
            await mqtt.asyncio_publish(topic, payload, retain=retain)

    mqtt.Disconnect()
