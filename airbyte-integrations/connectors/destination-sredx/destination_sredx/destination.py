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
from .db.connection import setup_database
from .process.process import StreamContext, Process
from .process.process_registry import ProcessRegistry, StreamName

logger = logging.getLogger("airbyte")


class DestinationSredx(Destination):

    def __init__(self):
        super().__init__()
        setup_database()
   
    def write(
        self, config: Mapping[str, Any], configured_catalog: ConfiguredAirbyteCatalog, input_messages: Iterable[AirbyteMessage]
    ) -> Iterable[AirbyteMessage]:
        # payloads=[]
        # logger.info(f"config ---------- {config}")
        # logger.info(f"configured cataglog : {configured_catalog}")
        # logger.info(f"input_messages : {input_messages}")

        origin = self.get_origin(config=config, catalog=configured_catalog)
        streamContext = StreamContext(
            origin=origin,
            logger=logger,
            config=config,
        )
        for message in input_messages:
            logger.info(f"message : ====== {message}")
            if message.type == Type.RECORD:
                if message.record is None:
                    raise ValueError(f"No record found for message {message}")
                if message.record.stream is None:
                    raise ValueError(f"No stream found for message {message}")
                record = message.record
                stream = record.stream
                logger.info(f"stream name {stream}")
                logger.info(f"stream name 1 {StreamName.from_string(stream)}")
                process = self.get_process(stream)
                logger.info(f"process {process}")
                process.run(
                    record,
                    streamContext
                )
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

    @staticmethod
    def get_process(stream: str) -> Process:
        process = ProcessRegistry.get_process(
            stream_name=StreamName.from_string(stream)
        )
        return process

        #
        # for message in input_messages:
        #     yield message
        #     if message.type == Type.RECORD:
        #         record=message.record
        #         emitted_at_datetime = datetime.datetime.fromtimestamp(record.emitted_at / 1000)
        #         emitted_at = emitted_at_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        #         git_repo=re.search(r'repos/(.*?)/pulls/.*',record.data['url']).group(1)
        #         logger.info(f"record ------------{record} ")
        #         merged_at = record.data['merged_at']
        #         created_at = record.data['created_at']
        #         ttm = self.calculate_time_difference(created_at,merged_at)
        #         payload = {
        #             "idPullRequest": str(record.data['id']),
        #             "gitRepo": git_repo,
        #             "createdAt": created_at,
        #             "closedAt": record.data['closed_at'],
        #             "mergedAt": merged_at,
        #             "state": record.data['state'],
        #             "emittedAt": emitted_at,
        #             "ttm": str(ttm)
        #         }
        #
        #         collection.insert_one(payload)
        #         payloads.append(payload)
        #         yield AirbyteMessage(type=Type.RECORD, record=record)



        # collection.insert_many(payloads)
        # response = requests.post(url, json={"source":"Git","metric":"TimeToMerge","data":payloads})



    # def calculate_time_difference(self, date_str1, date_str2):
    #     if not date_str1 or not date_str2:
    #         return None  # or raise ValueError("One of the dates is None")
    #
    #     format_str = '%Y-%m-%dT%H:%M:%SZ'  # This is the format of your date strings
    #     try:
    #         datetime_obj1 = datetime.datetime.strptime(date_str1, format_str)
    #         datetime_obj2 = datetime.datetime.strptime(date_str2, format_str)
    #     except ValueError as e:
    #         # Handle the case where the date format is incorrect
    #         return None  # or raise ValueError("Incorrect date format")
    #
    #     # Calculate the difference
    #     time_diff = datetime_obj2 - datetime_obj1
    #
    #     return int(time_diff.total_seconds())

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

    @staticmethod
    def get_origin(config: Mapping[str, Any], catalog: ConfiguredAirbyteCatalog) -> str:
        origin = config.get("origin")
        if origin:
            logger.info(f"Using origin '{origin}' found in config")
            return origin

        # Determine origin from stream prefixes
        origins = list(set(s.stream.name.split('__', 1)[0] for s in catalog.streams))
        if len(origins) == 0:
            raise ValueError('Could not determine origin from catalog')
        elif len(origins) > 1:
            raise ValueError(f"Found multiple possible origins from catalog: {','.join(origins)}")

        origin = origins[0]
        logger.info(f"Determined origin '{origin}' from stream prefixes")
        return origin
