from ..process import Process, StreamContext
from airbyte_cdk.models import AirbyteRecordMessage


class PullRequestsProcess(Process):

    def run(self, record: AirbyteRecordMessage, ctx: StreamContext):
        ctx.logger.info("Starting pull")


