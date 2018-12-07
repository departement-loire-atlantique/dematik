# coding: utf8
from test_condition_parser import ConditionParserTester
import unittest

class ConditionEmptyTest(ConditionParserTester):

    def test_empty(self):
        self.check('''
            si x1 est vide alors afficher le message m1
            ''', 'm1',
            [
                (True,  {'form_var_x1': None   }),
                (True,  {'form_var_x1': []     }),
                (True,  {'form_var_x1': ""     }),
                (False, {'form_var_x1': "a"    }),
                (False, {'form_var_x1': ['e'] })
            ]
        )

    def test_filled(self):
        self.check('''
            si x1 est coché alors afficher le message m1
            ''', 'm1',
            [
                (False,  {'form_var_x1': None   }),
                (False,  {'form_var_x1': []     }),
                (False,  {'form_var_x1': ""     }),
                (True, {'form_var_x1': "a"    }),
                (True, {'form_var_x1': ['e'] })
            ]
        )
        
if __name__ == '__main__':
    unittest.main()