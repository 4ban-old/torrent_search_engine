import coverage

import Pudge.tests as t


import unittest

loader = unittest.TestLoader()
suite = loader.loadTestsFromModule(t.tests_tools)

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)


