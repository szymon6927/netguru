from abc import ABC
from abc import abstractmethod


class Discount(ABC):
    @abstractmethod
    def calculate_discount(self, price: int):
        pass


class NoDiscount(Discount):
    def calculate_discount(self, price):
        return 0


class DiscountCoupon(Discount):
    def calculate_discount(self, price):
        if price > 20:
            return 10
        else:
            return 0


class BlackFirday(Discount):
    def calculate_discount(self, price):
        return price * 0.3


class ProgressDiscount(Discount):
    def calculate_discount(self, price):
        if price > 50:
            return price * 0.20
        elif 10 < price <= 50:
            return price * 0.10
        else:
            return price * 0.05


class Checkout:
    def __init__(self, price: int, discount: Discount):
        self.price = price
        self.discount = discount

    def get_total_price(self):
        return self.price - self.discount.calculate_discount(self.price)


class CheckoutFactory:
    @staticmethod
    def create(price: int, discount_type: str):
        mapper = {
            'coupon': DiscountCoupon(),
            'black_friday': BlackFirday(),
            'progress': ProgressDiscount()
        }

        if discount_type not in mapper:
            raise KeyError('Unknown discount type')

        return Checkout(price, mapper[discount_type])


def main():
    checkout = CheckoutFactory.create(100, 'coupon')
    print(f'Total price: {checkout.get_total_price()}')


if __name__ == '__main__':
    main()
