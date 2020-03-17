import abc
import uuid
import typing

from dataclasses import asdict

from src.entities import EventStream
from src.entities import Event


class EventStoreRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load_stream(self, aggregate_uuid: uuid.UUID) -> EventStream:
        pass

    @abc.abstractmethod
    def append_to_stream(
            self,
            aggregate_uuid: uuid.UUID,
            expected_version: typing.Optional[int],
            events
    ) -> None:
        pass


class FileStorageEventStore(EventStoreRepository):
    AGGREGATES = []
    EVENTS = []

    def load_stream(self, aggregate_uuid: uuid.UUID) -> EventStream:
        pass

    def append_to_stream(
            self,
            aggregate_uuid: str,
            expected_version: typing.Optional[int],
            events
    ) -> None:
        for event in events:
            self.EVENTS.append(
                Event(
                    uuid=str(uuid.uuid4()),
                    aggregate_uuid=str(aggregate_uuid),
                    name=event.__class__.__name__,
                    data=asdict(event)
                )
            )

    def list(self):
        result = [asdict(event) for event in self.EVENTS]
        return result
