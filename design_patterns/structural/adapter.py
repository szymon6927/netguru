class Target:
    def method_a(self):
        print("Target: method_a")


class Adaptee:
    def method_b(self):
        print("Adaptee: method_b")


class Adapter(Target):
    def method_a(self):
        adaptee = Adaptee()
        adaptee.method_b()

# --------------------------------------------------------


class OldXML:
    def write_xml(self):
        # some old stuff here
        pass


class NewXML:
    def xml(self):
        print("New XML")


class XML(OldXML):
    def write_xml(self):
        adaptee = NewXML()
        adaptee.xml()


def main_1():
    client = Adapter()
    client.method_a()


def main_2():
    client = XML()
    client.write_xml()


if __name__ == '__main__':
    main_1()
    print("")
    main_2()
