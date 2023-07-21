import zmq
import asyncio

from functions import recv_and_process

ctx = zmq.asyncio.Context()

config = {
    "/RIG/InfoPlusDVSInterface4": {
        "paths": [
            "/ns1:PutReisInformatieBoodschapIn/ns2:ReisInformatieProductDVS/ns2:DynamischeVertrekStaat/ns2:RitDatum",
            "/ns1:PutReisInformatieBoodschapIn/ns2:ReisInformatieProductDVS/ns2:DynamischeVertrekStaat/ns2:RitId",
            "/ns1:PutReisInformatieBoodschapIn/ns2:ReisInformatieProductDVS/ns2:DynamischeVertrekStaat/ns2:RitStation/ns2:StationCode"
        ],
        "namespaces": {"ns1": "urn:ndov:cdm:trein:reisinformatie:messages:5", "ns2": "urn:ndov:cdm:trein:reisinformatie:data:4"},
        "topic_prefix": "train/departure/"
    }
}

asyncio.run(recv_and_process(ctx, "7664", "ns", config))

