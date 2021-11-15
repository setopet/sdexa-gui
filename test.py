from sys import stdout
from unittest import TestLoader, TextTestRunner
import backend
import server


def load_tests(module):
    return TestLoader().loadTestsFromModule(module)


def run_tests(module):
    test_runner = TextTestRunner(verbosity=2, stream=stdout)
    tests = load_tests(module)
    print("Running tests for " + str(module))
    print("----------------------------------------------------------------------")
    test_runner.run(tests)
    print("\n")


if __name__ == '__main__':
    run_tests(server)
    run_tests(backend)
    exit()
