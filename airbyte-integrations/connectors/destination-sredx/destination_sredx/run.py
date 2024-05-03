#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from .destination import DestinationSredx

def run():
    destination = DestinationSredx()
    destination.run(sys.argv[1:])
