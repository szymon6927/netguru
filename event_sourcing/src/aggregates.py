from src.events import OrderCreated
from src.events import StatusChanged


class OrderAggregate:
    def __init__(self, events: list):
        for event in events:
            self.apply(event)

        self.changes = []

    @classmethod
    def create(cls, user_id: int):
        initial_event = OrderCreated(user_id)
        instance = cls([initial_event])
        instance.changes = [initial_event]
        return instance

    def apply(self, event):
        if isinstance(event, OrderCreated):
            self.user_id = event.user_id
            self.status = 'new'
        elif isinstance(event, StatusChanged):
            self.status = event.new_status
        else:
            raise ValueError('Unknown event!')

    def set_status(self, new_status: str):
        if new_status not in ('new', 'paid', 'confirmed', 'shipped'):
            raise ValueError(f'{new_status} is not a correct status!')

        event = StatusChanged(new_status)
        self.apply(event)
        self.changes.append(event)
