from ..process import Process, StreamContext
from airbyte_cdk.models import AirbyteRecordMessage


class PullRequests(Process):
    def run(self, record: AirbyteRecordMessage, ctx: StreamContext):
        print("comments")
