class MetaSingleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


class Singleton(metaclass=MetaSingleton):
    pass


def main():
    s1 = Singleton()
    s2 = Singleton()

    print(id(s1))
    print(id(s2))

    if id(s1) == id(s2):
        print("Singleton works")


if __name__ == '__main__':
    main()
