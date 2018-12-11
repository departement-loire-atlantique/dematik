# coding: utf8
from test_condition_parser import ConditionParserTester
import unittest

class ConditionHideTest(ConditionParserTester):

    def test_message(self):
        self.check('si x1 est égal à 1 alors masquer cette page', None,
            [ (True, {'form_var_x1':1 }) ]
        )

if __name__ == '__main__':
    unittest.main()