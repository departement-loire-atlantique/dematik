# coding: utf8
from condition_parser import ConditionParser
from jinja2 import Environment
import unittest

class ConditionParserTester(unittest.TestCase):

    def setUp(self):
        self.c = ConditionParser()

    def check(self, expression, data, test_datas):
        condition = self.c.parse(expression)
        if condition.type == 'CONDTION_MESSAGE' and data:
            self.assertEqual(condition.getMessage(), data)
        elif condition.type == 'CONDITION_HIDE_FIELD' and data:
            self.assertEqual(condition.getHiddenFieldname(), data)

        for i, test_data in enumerate(test_datas):
            result, test_vars = test_data
            expr_python = condition.build('python')
            self.assertEqual(eval(expr_python, test_vars), result, "case python %s, expression : %s" % (i+1, expr_python))

            expr_django = condition.build('django')
            test_code = "{% if " + expr_django + " %}True{% else %}False{% endif %}"
            test_result = "False"
            try:
                test_result = Environment().from_string(test_code).render(test_vars)
            except:
                pass
            test_awaited = "True" if result else "False"
            self.assertEqual(test_result, test_awaited, "case django %s, expression : %s, returns: %s, awaited: %s" % (i+1, expr_django, test_result, test_awaited))


class ConditionParserTest(ConditionParserTester):

    def test_invalid(self):
        with self.assertRaises(Exception):
            self.c.parse("nothing good")

    def test_partially_invalid(self):
        with self.assertRaises(Exception):
            self.c.parse("if partially good alors")

if __name__ == '__main__':
    unittest.main()