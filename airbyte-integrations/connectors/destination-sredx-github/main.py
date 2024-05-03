#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#


import sys

from destination_sredx_github import DestinationSredxGithub

if __name__ == "__main__":
    DestinationSredxGithub().run(sys.argv[1:])  
