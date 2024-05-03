#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#


import sys

from destination_sredx import DestinationSredx

if __name__ == "__main__":
    DestinationSredx().run(sys.argv[1:])
