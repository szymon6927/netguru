from abc import ABC
from abc import abstractmethod


class User(ABC):
    pass


class PrivatePerson(User):
    def __init__(self, pesel_number):
        self.pesel_number = pesel_number

    def __str__(self):
        return 'Private person'


class Company(User):
    def __init__(self, nip):
        self.nip = nip

    def __str__(self):
        return 'Company user'


class UserFactory(ABC):
    def create_from(self, data):
        raise NotImplementedError


class MultipleUserTypeFactory(UserFactory):
    def create_from(self, data):
        if 'nip' in data:
            return Company(data.get('nip'))

        if 'pesel' in data:
            return PrivatePerson(data.get('pesel'))

        raise ValueError('Data required to create User needs to have PESEL or NIP')


class UserRegistrationService:
    def __init__(self, factory: UserFactory):
        self.user_factory = factory

    def register(self, data: dict):
        user = self.user_factory.create_from(data)
        return user


def main():
    data = {
        'nip': 8411018492
    }

    factory = MultipleUserTypeFactory()
    registration_service = UserRegistrationService(factory)
    user = registration_service.register(data)

    print(f'Created user = {user}')


if __name__ == '__main__':
    main()
