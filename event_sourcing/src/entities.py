import typing
from dataclasses import dataclass


@dataclass
class Event:
    uuid: str
    aggregate_uuid: str
    name: str
    data: dict


@dataclass
class EventStream:
    uuid: str
    events: typing.List[Event]
    version: int


@dataclass
class Aggregate:
    uuid: str
    version: int

