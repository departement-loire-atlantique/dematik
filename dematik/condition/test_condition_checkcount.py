# coding: utf8
from test_condition_parser import ConditionParserTester
import unittest

class ConditionEmptyTest(ConditionParserTester):

    def test_one(self):
        self.check('''
           si moins de 1 élément de x1 est coché
           alors afficher le message m1
            ''', 'm1',
            [
                (True, {'form_var_x1':None }),
                (True, {'form_var_x1':[] }),
                (False, {'form_var_x1':["a"] }),
                (False, {'form_var_x1':["a", "b"] }),
            ]
        )

    def test_multi(self):
        self.check('''
           si moins de 3 éléments de x1 sont cochés
           alors afficher le message m1
            ''', 'm1',
            [
                (True, {'form_var_x1':None }),
                (True, {'form_var_x1':[] }),
                (True, {'form_var_x1':["a"] }),
                (True, {'form_var_x1':["a", "b"] }),
                (False, {'form_var_x1':["a", "b", "c"] }),
                (False, {'form_var_x1':["a", "b", "c", "d"] }),
            ]
        )

    def test_plus_one(self):
        self.check('''
           si au moins 1 élément de x1 est coché
           alors afficher le message m1
            ''', 'm1',
            [
                (False, {'form_var_x1':None }),
                (False, {'form_var_x1':[] }),
                (True, {'form_var_x1':["a"] }),
                (True, {'form_var_x1':["a", "b"] }),
            ]
        )

    def test_plus_multi(self):
        self.check('''
           si au moins 3 éléments de x1 sont cochés
           alors afficher le message m1
            ''', 'm1',
            [
                (False, {'form_var_x1':None }),
                (False, {'form_var_x1':[] }),
                (False, {'form_var_x1':["a"] }),
                (False, {'form_var_x1':["a", "b"] }),
                (True, {'form_var_x1':["a", "b", "c"] }),
                (True, {'form_var_x1':["a", "b", "c", "d"] }),
            ]
        )

if __name__ == '__main__':
    unittest.main()