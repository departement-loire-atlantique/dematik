# coding: utf8
from test_condition_parser import ConditionParserTester
import unittest

class ConditionEmptyTest(ConditionParserTester):

    def test_not_empty(self):
        self.check('''
            si x1 n'est pas vide alors afficher le message m1
            ''', 'm1',
            [
                (False,  {'form_var_x1': None   }),
                (False,  {'form_var_x1': []     }),
                (False,  {'form_var_x1': ""     }),
                (True, {'form_var_x1': "a"    }),
                (True, {'form_var_x1': ['e'] })
                
            ]
        )

    def test_not_filled(self):
        self.check('''
            si x1 n'est pas coché alors afficher le message m1
            ''', 'm1',
            [
                (True,  {'form_var_x1': None   }),
                (True,  {'form_var_x1': []     }),
                (True,  {'form_var_x1': ""     }),
                (False, {'form_var_x1': "a"    }),
                (False, {'form_var_x1': ['e'] })
            ]
        )
    
    def test_not_equal(self):
        self.check('''si x1 n'est pas égal à x2 alors afficher le message m1''', 'm1',
            [
                (False, {'form_var_x1':None , 'form_var_x2':None}),
                (True, {'form_var_x1':None , 'form_var_x2':"b" }),
                (True, {'form_var_x1':3 , 'form_var_x2':"b" }),
                (True, {'form_var_x1':"a"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':"b"  , 'form_var_x2':"b" }), 
                (True, {'form_var_x1':2  , 'form_var_x2':3 }), 
                (False, {'form_var_x1':3  , 'form_var_x2':3 }), 
            ]
        )

        self.check('''si x1 n'est pas égal à "b" alors afficher le message m1''', 'm1',
            [
                (True, {'form_var_x1':None }),
                (True, {'form_var_x1':5    }),
                (True, {'form_var_x1':"a"  }), 
                (False, {'form_var_x1':"b"  }), 
            ]
        )

        self.check('''si x1 n'est pas égal à 5 alors afficher le message m1''', 'm1',
            [
                (True, {'form_var_x1':None }),
                (True, {'form_var_x1':3    }),
                (False, {'form_var_x1':5    }),
                (True, {'form_var_x1':"a"  }), 
            ]
        )

if __name__ == '__main__':
    unittest.main()