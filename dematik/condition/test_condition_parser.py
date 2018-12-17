# coding: utf8
from condition_parser import ConditionParser
import unittest

class ConditionParserTester(unittest.TestCase):

    def setUp(self):
        self.c = ConditionParser()

    def check(self, expression, data, test_datas):
        python_condition = self.c.parse(expression)
        if python_condition.type == 'CONDTION_MESSAGE' and data:
            self.assertEqual(python_condition.getMessage(), data)
        elif python_condition.type == 'CONDITION_HIDE_FIELD' and data:
            self.assertEqual(python_condition.getHiddenFieldname(), data)

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