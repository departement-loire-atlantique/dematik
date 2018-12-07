# coding: utf8
from test_condition_parser import ConditionParserTester
import unittest

class ConditionEmptyTest(ConditionParserTester):

    def test_message(self):
        self.check('si x1 est égal à x1 alors afficher le message m1', 'm1',
            [ (True, {'form_var_x1':1 }) ]
        )

        self.check('si x1 est égal à x1 alors afficher le message "message a complété"', 
            '"message a complété"',
            [ (True, {'form_var_x1':1 }) ]
        )

if __name__ == '__main__':
    unittest.main()