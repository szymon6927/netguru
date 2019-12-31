class SubSystem1:
    def do_something(self):
        print("SubSystem1 do something")


class SubSystem2:
    def do_something_epic(self):
        print("SubSystem2 do something epic")


class SubSystem3:
    def do_something_amazing(self):
        print("SubSystem3 do something amazing")


class Facade:
    def __init__(self):
        self.sub_system_1 = SubSystem1()
        self.sub_system_2 = SubSystem2()
        self.sub_system_3 = SubSystem3()

    def do_complex_operation(self):
        self.sub_system_1.do_something()
        self.sub_system_2.do_something_epic()
        self.sub_system_3.do_something_amazing()


def main():
    facade = Facade()
    facade.do_complex_operation()


if __name__ == '__main__':
    main()


