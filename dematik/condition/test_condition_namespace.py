# coding: utf8
from test_condition_parser import ConditionParserTester
import unittest

class ConditionNamespaceTest(ConditionParserTester):

    def test_namespace(self):
        self.check('''
            si namespace:x1 est vide alors afficher le message m1
            ''', 'm1',
            [
                (True,  {'form_var_namespace___x1': ""     }),
                (False, {'form_var_namespace___x1': "a"    }),
            ]
        )

    def test_namespace_underscore(self):
        self.check('''
            si namespace_under:x1_under est vide alors afficher le message m1
            ''', 'm1',
            [
                (True,  {'form_var_namespace_under___x1_under': ""     }),
                (False, {'form_var_namespace_under___x1_under': "a"    }),
            ]
        )
        
if __name__ == '__main__':
    unittest.main()