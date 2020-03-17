import uuid

from flask import Flask
from flask import jsonify

from random import randint

from src.entities import Aggregate
from src.repositories import FileStorageEventStore
from src.events import StatusChanged
from src.events import OrderCreated

app = Flask(__name__)


aggregate = Aggregate(
    uuid=str(uuid.uuid4()),
    version=1
)

event_store = FileStorageEventStore()


@app.route('/buy-product')
def buy_product():
    event_store.append_to_stream(aggregate.uuid, 1, [OrderCreated(user_id=randint(1, 100))])

    return 'Product bought'


@app.route('/order-confirmed')
def order_confirmed():
    event_store.append_to_stream(aggregate.uuid, 1, [StatusChanged('confirmed')])

    return 'Order confirmed'


@app.route('/order-paid')
def order_paid():
    event_store.append_to_stream(aggregate.uuid, 1, [StatusChanged('paid')])

    return 'Order paid'


@app.route('/order-shipped')
def order_shipped():
    event_store.append_to_stream(aggregate.uuid, 1, [StatusChanged('shipped')])

    return 'Order shipped'


@app.route('/order-history')
def order_history():
    return jsonify(event_store.list())


if __name__ == '__main__':
    app.run()
