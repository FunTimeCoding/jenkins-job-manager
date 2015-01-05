from lib.example_class import ExampleClass


def tests_can_be_functions():
    ec = ExampleClass()
    assert ec.run() == 0
