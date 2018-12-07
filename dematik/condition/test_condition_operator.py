# coding: utf8
from test_condition_parser import ConditionParserTester
import unittest

class ConditionEmptyTest(ConditionParserTester):

    def test_and(self):
        self.check('''
            si x1 est vide 
            et x2 est vide 
            et x3 est vide
            et x4 est vide
            alors afficher le message m1
            ''', 'm1',
            [
                (True, {'form_var_x1':None, 'form_var_x2':"", 'form_var_x3':[], 'form_var_x4':None}),
                (False, {'form_var_x1':None, 'form_var_x2':"a", 'form_var_x3':None, 'form_var_x4':None})
            ]
        )

    def test_or(self):
        self.check('''
            si x1 est vide 
            ou x2 est vide 
            ou x3 est vide
            ou x4 est vide
            alors afficher le message m1_m2
            ''', 'm1_m2',
            [
                (True, {'form_var_x1':"", 'form_var_x2':"", 'form_var_x3':[], 'form_var_x4':None}),
                (True, {'form_var_x1':"a", 'form_var_x2':"", 'form_var_x3':[], 'form_var_x4':None}),
                (True, {'form_var_x1':"a", 'form_var_x2':"b", 'form_var_x3':[], 'form_var_x4':None}),
                (False, {'form_var_x1':"a", 'form_var_x2':"a", 'form_var_x3':"a", 'form_var_x4':"a"})
            ]
        )
    
if __name__ == '__main__':
    unittest.main()