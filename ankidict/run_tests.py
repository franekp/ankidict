#!/usr/bin/env python
import os
import __init__
from unittest import TestLoader, runner

this_dir = os.path.dirname(__file__)

dirs = ["addon", "libdict", "pagemodel"]

loader = TestLoader()

tests = [loader.discover(os.path.join(this_dir, d), top_level_dir=this_dir) for d in dirs]

testRunner = runner.TextTestRunner()
for test in tests:
    testRunner.run(test)