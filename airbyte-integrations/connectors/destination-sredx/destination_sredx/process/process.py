import json
from collections import defaultdict
from typing import Any, Dict, Generic, List, Optional, TypeVar, Mapping
from logging import Logger
from airbyte_cdk.models import AirbyteRecordMessage

from ..lib.utils import to_snake_case

# Type variable for generic typing
R = TypeVar('R', bound=Dict[str, Any])


class StreamName:
    def __init__(self, source: str, name: str):
        self.source = source
        self.name = name
        self.str = None

    @property
    def as_string(self) -> str:
        if not self.str:
            self.str = f"{self.source.lower()}__{self.name}"
        return self.str

    @staticmethod
    def from_string(s: str):
        if not s:
            raise ValueError(f"Empty stream name {s}")
        parts = s.split('__')
        if len(parts) < 2:
            raise ValueError(f"Invalid stream name {s}: missing source prefix (e.g 'github__')")
        if len(parts[-1]) < 3:
            parts = split_with_limit(s, '__', len(parts) > 3 and 3 or 2)
        return StreamName(parts[-2], parts[-1])


def split_with_limit(s: str, separator: str, limit: int) -> List[str]:
    parts = s.split(separator)
    if len(parts) <= limit:
        return parts
    limited_parts = parts[:limit-1]
    remainder = separator.join(parts[limit-1:])
    limited_parts.append(remainder)
    return limited_parts


class StreamContext:
    def __init__(self, logger: Logger, config: Mapping[str, Any], origin: Optional[str] = None):
        self.logger = logger
        self.config = config
        self.origin = origin
        self.records_by_stream_name = defaultdict(dict)

    def get_all(self, stream_name: str) -> Dict[str, AirbyteRecordMessage]:
        return self.records_by_stream_name[stream_name]

    def get(self, stream_name: str, id: str) -> Optional[AirbyteRecordMessage]:
        return self.records_by_stream_name[stream_name].get(id)

    def set(self, stream_name: str, id: str, record: AirbyteRecordMessage):
        self.records_by_stream_name[stream_name][id] = record


class ProcessTyped(Generic[R]):
    def __init__(self):
        self.stream = None

    @property
    def stream_name(self) -> StreamName:
        if self.stream:
            return self.stream

        self.stream = StreamName.from_string(f"{self.source}__{to_snake_case(self.__class__.__name__)}")
        return self.stream

    @property
    def dependencies(self) -> List[StreamName]:
        return []

    def id(self, record: AirbyteRecordMessage) -> Any:
        raise NotImplementedError

    @property
    def destination_models(self) -> List[str]:
        raise NotImplementedError

    def run(self, record: AirbyteRecordMessage, ctx: StreamContext) -> List[Dict]:
        raise NotImplementedError

    async def on_processing_complete(self, ctx: StreamContext) -> List[Dict]:
        return []


class Process(ProcessTyped[Dict[Any, Any]]):
    pass


def parse_object_config(obj: Any, name: str) -> Any:
    if not obj:
        return None
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, str):
        try:
            return json.loads(obj)
        except Exception as e:
            raise ValueError(f"Could not parse JSON object from {name} {obj}. Error: {e}")
    raise ValueError(f"{name} must be a JSON object or stringified JSON object")
