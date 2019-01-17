# coding: utf8
from condition_parser import ConditionParser
import django
from django.template import Context, Template
from django.conf import settings
import unittest

class ConditionParserTester(unittest.TestCase):

    def setUp(self):
        self.c = ConditionParser()
        if not settings.configured:
            settings.configure(TEMPLATES=[
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'APP_DIRS': False, # we have no apps
                }])
            django.setup()
        

    def check(self, expression, data, test_datas):
        condition = self.c.parse(expression)
        if condition.type == 'CONDTION_MESSAGE' and data:
            self.assertEqual(condition.getMessage(), data)
        elif condition.type == 'CONDITION_HIDE_FIELD' and data:
            self.assertEqual(condition.getHiddenFieldname(), data)

        for i, test_data in enumerate(test_datas):
            result, test_vars = test_data
            test_vars_debug = ["%s : %s" % t for t in test_vars.items()]
            test_awaited = "True" if result else "False"
            expr_python = condition.build('python')
            test_result = eval(expr_python, test_vars)
            self.assertEqual(test_result, result, "case python %s, expression : %s, vars: %s, returns: %s, awaited: %s" % (i+1, expr_python, test_vars_debug, test_result, test_awaited))
            expr_django = condition.build('django')
            test_code = Template('{% if ' + expr_django + ' %}True{% else %}False{% endif %}')
            test_result = "False"
            try:
                context = Context(test_vars)
                test_result = test_code.render(context)
            except:
                pass
            
            self.assertEqual(test_result, test_awaited, "case django %s, expression : %s, vars: %s, returns: %s, awaited: %s" % (i+1, expr_django, test_vars_debug, test_result, test_awaited))


class ConditionParserTest(ConditionParserTester):

    def test_invalid(self):
        with self.assertRaises(Exception):
            self.c.parse("nothing good")

    def test_partially_invalid(self):
        with self.assertRaises(Exception):
            self.c.parse("if partially good alors")

if __name__ == '__main__':
    unittest.main()