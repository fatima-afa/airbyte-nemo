from typing import Dict, Optional, Callable
import importlib
from collections import defaultdict
from .process import StreamName, Process
import logging
import os

# Get the current working directory
current_directory = os.getcwd()

logger = logging.getLogger("airbyte")

# class Process:
#     def __init__(self, stream_name):
#         self.stream_name = stream_name


class ProcessRegistry:
    processes_by_stream: Dict[str, Process or bool] = defaultdict(bool)

    @staticmethod
    def get_process(stream_name: StreamName) -> Optional[Process]:
        logger.info(f"place : {current_directory}")
        name = stream_name.as_string
        res = ProcessRegistry.processes_by_stream[name]
        logger.info(f"res : {res}")
        logger.info(f"name : {name}")
        if res and isinstance(res, Process):
            logger.info(f"here ")
            return res
        if res:
            logger.info(f"here 2")
            return None

        try:
            process_dir = stream_name.source.replace('_', '-')
            mod = importlib.import_module(f'.process.{process_dir}.{stream_name.name}', package='destination_sredx')
            logger.info(f"mod : {mod}")

            class_name = ''.join(word.capitalize() for word in stream_name.name.split('_'))
            logger.info(f"class_name : {class_name}")

            process_class = getattr(mod, class_name, None)
            if not process_class:
                raise ValueError(f"Could not find process from module for stream {name}")

            process = process_class()
            logger.info(f"process - process registry : {process}")

            ProcessRegistry.processes_by_stream[name] = process
            return process
        except Exception as e:
            ProcessRegistry.processes_by_stream[name] = True
            logger.info(f"here 3 {e}")
            return None

    @staticmethod
    def add_process(process: Process):
        name = process.stream_name.as_string
        ProcessRegistry.processes_by_stream[name] = process
