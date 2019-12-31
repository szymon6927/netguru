from abc import ABC
from abc import abstractmethod
from random import randrange


class Observer(ABC):
    @abstractmethod
    def update(self, subject) -> None:
        pass


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def notify(self):
        pass

    @abstractmethod
    def get_state(self):
        pass


class ConcreteSubject(Subject):
    _state = None
    _observers = []

    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def get_state(self):
        return self._state

    def some_business_logic(self) -> None:
        print("\nSubject: I'm doing something important.")
        self._state = randrange(0, 10)

        print(f"Subject: My state has just changed to: {self._state}")
        self.notify()


class ConcreteObserverA(Observer):
    def update(self, subject: Subject) -> None:
        if subject.get_state() < 3:
            print("ConcreteObserverA: Reacted to the event")


class ConcreteObserverB(Observer):
    def update(self, subject: Subject) -> None:
        if subject.get_state() == 0 or subject.get_state() >= 2:
            print("ConcreteObserverB: Reacted to the event")


def main():
    subject = ConcreteSubject()

    observer_a = ConcreteObserverA()
    subject.attach(observer_a)

    observer_b = ConcreteObserverB()
    subject.attach(observer_b)

    subject.some_business_logic()
    subject.some_business_logic()

    subject.detach(observer_a)

    subject.some_business_logic()


if __name__ == "__main__":
    main()
