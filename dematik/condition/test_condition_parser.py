# coding: utf8
from condition_parser import ConditionParser
import unittest

class ConditionParserTester(unittest.TestCase):

    def setUp(self):
        self.c = ConditionParser()

    def check(self, expression, message, test_datas):
        python_condition = self.c.parse(expression)
        if message:
            self.assertEqual(python_condition.getMessage(), message)
        for i, test_data in enumerate(test_datas):
            result, test_vars = test_data
            expr = python_condition.build()
            self.assertEqual(eval(expr, test_vars), result, "case %s, expression : %s" % (i+1, expr))

class ConditionParserTest(ConditionParserTester):

    def test_invalid(self):
        with self.assertRaises(Exception):
            self.c.parse("nothing good")

    def test_partially_invalid(self):
        with self.assertRaises(Exception):
            self.c.parse("if partially good alors")

if __name__ == '__main__':
    unittest.main()