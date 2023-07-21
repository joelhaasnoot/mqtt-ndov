# MQTT-NDOV

This repo contains scripts that bridge Dutch Public Transit messages from ZMQ to MQTT and offers some nice additional features. 
Stichting OpenGeo provides [NDOV-Loket](https://ndovloket.nl) and provides feeds over ZMQ that these scripts listen to and forward over MQTT.

## User Manual
A staging server is offered on [mqtt.joelhaasnoot.nl](http://mqtt.joelhaasnoot.nl). Use the following notes to understand how the data is structured.

### Raw Topics

The following topics forward the raw stream of messages
- Train data from [NS](http://ns.nl) is fed as `ns/<original zmq topic>`, as a stream. In practice this means:
  - `ns/RIG/InfoPlusDVSInterface4` -> Stream of DVS messages ("dynamic departure message" - per service, per stops)
  - `ns/RIG/InfoPlusDASInterface4` -> Stream of DAS messages ("dynamic arrival message" - per service, per stop)
  - `ns/RIG/InfoPlusDASInterface4` -> Stream of RIT messages (complete trip details, per service, all stops)
  - `ns/RIG/NStreinpositiesInterface5` -> Stream of train GPS positions
  - and some others (mainly messages related to disruptions)
- Other transit operators use [BISON](https://bison.dova.nu/) standards. In practice:
  - `bison/ARR/KV6posinfo` - Arriva KV6 (position) messages
  - `bison/ARR/KV17cvlinfo` - Arriva KV17 (service change) messages
  - `bison/ARR/KV17cvlinfo` - Arriva KV17 (service change) messages
  - And these three topics repeated for the operators `QBUZZ`, `CXX`, `KEOLIS`, `IVU` (supplier for Qbuzz), `RIG` (supplier for HTM, RET), `GVB`, `EBS`, `OPENOV` (supplies TEC)
- SIRI feeds from transit operators are fed as `siri/<original zmq topic>`. Again, in practice:
  - `siri/GVB/EstimatedTimetableDelivery` - SIRI EstimatedTimetable for GVB (Amsterdam)
  - `siri/GVB/VehicleMonitoringDelivery` - SIRI VehicleMonitoring for GVB (Amsterdam)

### Structured Topics

Details to follow

### Other notes

- It is possible to use Quality of Service (QoS) level 1 to make sure you don't miss messages. If this leads to performance issues, this will be disabled or restricted to registered users
- For the non _stream topics_, the latest message is retained. This is so that you can (re)connect and find a message, as long as you know the topic you're looking for. 
- The messages expire however after about a day
- Currently, there is no implementation over SSL on the staging server


## Admin Manual
To run on your own server - change config.py or create local_config.py and specify the options. `scripts/` contains systemctl unit files. 
