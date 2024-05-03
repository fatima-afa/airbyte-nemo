#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#


import sys

from destination_nemo import DestinationNemo

if __name__ == "__main__":
    DestinationNemo().run(sys.argv[1:])
