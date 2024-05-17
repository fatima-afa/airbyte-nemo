#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#
from typing import Any, Iterable, Mapping
import requests
import datetime
import re
from airbyte_cdk import AirbyteLogger
from airbyte_cdk.destinations import Destination
from airbyte_cdk.models import AirbyteConnectionStatus, AirbyteMessage, ConfiguredAirbyteCatalog, Status, Type
import logging
logger = logging.getLogger("airbyte")

class DestinationSredx(Destination):

    # def serialize_message(self,message):
    # # Serialize the AirbyteMessage object to a dictionary
    #     if message.type == Type.RECORD and message.record is not None:
    #         return {
    #             'object': message.record.data,
    #             # Add other fields as needed
    #         }
    #     return {}
    
    # def convert_to_json_string(self,messages):
    #     # Serialize each message to a dictionary
    #     serialized_messages= [self.serialize_message(message) for message in messages]
    #     # Convert the list of dictionaries to a JSON string
    #     return json.dumps(serialized_messages)
   
    def write(
        self, config: Mapping[str, Any], configured_catalog: ConfiguredAirbyteCatalog, input_messages: Iterable[AirbyteMessage]
    ) -> Iterable[AirbyteMessage]:
        # streams = {s.stream.name for s in configured_catalog.streams}
        # client_id = config.get("client_id")
        # client_secret = config.get("client_secret")
        # # Assuming your endpoint requires Basic Authentication
        # auth = (client_id, client_secret)
        # headers = {'Content-Type': 'application/json'}
        # # self.integration = config.get("integration")
        # target_stream = config.get("target_stream")
        # message_pull_requests=[]
        # if target_stream == "pull_requests":
        # message_pull_requests = self.convert_to_json_string(input_messages)
        url = "http://localhost:8080/api/v2/webHooks/metrics"
        payloads=[]
        target_stream = config.get("target_stream") 
        if(target_stream =="TimeToMerge"):
            for message in input_messages:
                if message.type == Type.RECORD:
                    record=message.record   
                    emitted_at_datetime = datetime.datetime.fromtimestamp(record.emitted_at / 1000)  
                    emitted_at = emitted_at_datetime.strftime('%Y-%m-%dT%H:%M:%S')
                    git_repo=re.search(r'repos/(.*?)/pulls/.*',record.data['url']).group(1)
                    logger.info(f"record ------------{record} ")
                    payload = {
                        "idPullRequest": str(record.data['id']),
                        "gitRepo": git_repo,
                        "createdAt": record.data['created_at'],
                        "closedAt": record.data['closed_at'],
                        "mergedAt": record.data['merged_at'],
                        "state": record.data['state'],
                        "emittedAt": emitted_at
                    }

                    payloads.append(payload)
                    yield AirbyteMessage(type=Type.RECORD, record=record)

        response = requests.post(url, json={"source":"Git","metric":"TimeToMerge","data":payloads})

        """
        TODO
        Reads the input stream of messages, config, and catalog to write data to the destination.

        This method returns an iterable (typically a generator of AirbyteMessages via yield) containing state messages received
        in the input message stream. Outputting a state message means that every AirbyteRecordMessage which came before it has been
        successfully persisted to the destination. This is used to ensure fault tolerance in the case that a sync fails before fully completing,
        then the source is given the last state message output from this method as the starting point of the next sync.

        :param config: dict of JSON configuration matching the configuration declared in spec.json
        :param configured_catalog: The Configured Catalog describing the schema of the data being received and how it should be persisted in the
                                    destination
        :param input_messages: The stream of input messages received from the source
        :return: Iterable of AirbyteStateMessages wrapped in AirbyteMessage structs
        """

        yield AirbyteMessage(type=Type.STATE, value="") 

    def check(self, logger: AirbyteLogger, config: Mapping[str, Any]) -> AirbyteConnectionStatus:
        """
        Tests if the input configuration can be used to successfully connect to the destination with the needed permissions
            e.g: if a provided API token or password can be used to connect and write to the destination.

        :param logger: Logging object to display debug/info/error to the logs
            (logs will not be accessible via airbyte UI if they are not passed to this logger)
        :param config: Json object containing the configuration of this destination, content of this json is as specified in
        the properties of the spec.json file

        :return: AirbyteConnectionStatus indicating a Success or Failure
        """
        try:
            # TODO

            return AirbyteConnectionStatus(status=Status.SUCCEEDED)
        except Exception as e:
            return AirbyteConnectionStatus(status=Status.FAILED, message=f"An exception occurred: {repr(e)}")
