#!/usr/bin/env python
import os
import __init__
from unittest import TestLoader, runner, TestSuite


this_dir = os.path.dirname(__file__)
dirs = ["pagemodel", "addon", "libdict"]


def iterate_tests(test_suite_or_case):
    """Iterate through all of the test cases in 'test_suite_or_case'."""
    try:
        suite = iter(test_suite_or_case)
    except TypeError:
        yield test_suite_or_case
    else:
        for test in suite:
            for subtest in iterate_tests(test):
                yield subtest


loader = TestLoader()
tests = TestSuite([loader.discover(os.path.join(this_dir, d), top_level_dir=this_dir) for d in dirs])
test_runner = runner.TextTestRunner()


def run_light():
    lighttests = []
    for test in iterate_tests(tests):
        if hasattr(test, "is_heavy") and test.is_heavy:
            pass
        else:
            lighttests.append(test)
    lighttests = TestSuite(lighttests)
    test_runner.run(lighttests)


def run_heavy():
    test_runner.run(tests)


def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-l", "--heavy",
                  action="store_true", dest="heavy", default=False,
                  help="run heavy tests also")
    (options, args) = parser.parse_args()
    heavy = options.heavy
    if heavy:
        run_heavy()
    else:
        run_light()


if __name__ == "__main__":
    main()
