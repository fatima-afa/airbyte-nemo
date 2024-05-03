#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#


from typing import Any, Iterable, Mapping
import requests
from airbyte_cdk import AirbyteLogger
from airbyte_cdk.destinations import Destination
from airbyte_cdk.models import AirbyteConnectionStatus, AirbyteMessage, ConfiguredAirbyteCatalog, Status, Type


class DestinationSredxGithub(Destination):
    def __init__(self, config):
        self.integration = config.get("integration")
        self.target_stream = config.get("target_stream")

    def write(
        self, config: Mapping[str, Any], configured_catalog: ConfiguredAirbyteCatalog, input_messages: Iterable[AirbyteMessage]
    ) -> Iterable[AirbyteMessage]:
        
        json_messages_pull_Requests = [] 
        json_messages_branches = [] 

        for message in input_messages:
            if message.type == Type.RECORD: 
                json_messages_pull_Requests.append(message.record)
    
        # if self.integration == "github":
        #     if self.target_stream == "pull_requests":
        #         for message in input_messages:
        #             json_messages_pull_Requests.append(message.record)
        #     elif self.target_stream == "branches":
        #         for message in input_messages:
        #             json_messages_branches.append(message.record)        
    
            
        response = requests.post("https://script.google.com/macros/s/AKfycbykKF25pYQxApZhQYuUp1yBReYP7QGnajFAUifH_EQ9zN_w5xS2hfHIpl-3-wFFwnm6/exec",json=json_messages_pull_Requests)
        response = requests.post("https://script.google.com/macros/s/AKfycbykKF25pYQxApZhQYuUp1yBReYP7QGnajFAUifH_EQ9zN_w5xS2hfHIpl-3-wFFwnm6/exec",json=json_messages_branches)

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

        pass

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
