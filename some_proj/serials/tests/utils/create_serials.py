from some_proj.serials.tests.factories.serial import SerialFactory


def create_serials(count):
    SerialFactory.create_batch(count)


def create_serial():
    return SerialFactory.create()
