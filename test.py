"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from sys import stdout
from unittest import TestLoader, TextTestRunner
from tests import *


def load_tests(module):
    return TestLoader().loadTestsFromModule(module)


def run_tests(test_module):
    print("RUNNING TESTS FOR " + str(test_module))
    print("----------------------------------------------------------------------")
    TextTestRunner(verbosity=2, stream=stdout).run(load_tests(test_module))
    print("\n")


if __name__ == '__main__':
    run_tests(server)
    run_tests(backend)
    exit()
