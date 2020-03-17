from dataclasses import dataclass


@dataclass
class OrderCreated:
    user_id: int

@dataclass
class StatusChanged:
    new_status: str
