# coding: utf8
from test_condition_parser import ConditionParserTester
import unittest

class ConditionCompareTest(ConditionParserTester):

    def test_equal_var(self):
        self.check('si x1 est égal à x2 alors afficher le message m1', 'm1',
            [
                (True, {'form_var_x1':None , 'form_var_x2':None}),
                (True, {'form_var_x1':"" , 'form_var_x2':""}),
                (False, {'form_var_x1':None , 'form_var_x2':"b" }),
                (False, {'form_var_x1':3 , 'form_var_x2':"b" }),
                (False, {'form_var_x1':"a"  , 'form_var_x2':"b" }), 
                (True, {'form_var_x1':"b"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':2  , 'form_var_x2':3 }), 
                (True, {'form_var_x1':3  , 'form_var_x2':3 }), 
                (True, {'form_var_x1':"3"  , 'form_var_x2':"3" }),
            ]
        )

    def test_equal_special(self):
        self.check('si x1 est égal à "bé" alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None }),
                (False, {'form_var_x1':5    }),
                (False, {'form_var_x1':"a"  }), 
                (True, {'form_var_x1':"b&#233;"  }), 
            ]
        )

    def test_equal_number(self):
        self.check('si x1 est égal à 53 alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None }),
                (False, {'form_var_x1':3    }),
                (True, {'form_var_x1':53    }),
                (True, {'form_var_x1':"53"    }),
                (False, {'form_var_x1':"a"  }), 
            ]
        )

    def test_different_var(self):
        self.check('si x1 est différent de x2 alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None , 'form_var_x2':None}),
                (False, {'form_var_x1':"" , 'form_var_x2':""}),
                (True, {'form_var_x1':None , 'form_var_x2':"b" }),
                (True, {'form_var_x1':3 , 'form_var_x2':"b" }),
                (True, {'form_var_x1':"a"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':"b"  , 'form_var_x2':"b" }), 
                (True, {'form_var_x1':2  , 'form_var_x2':3 }), 
                (False, {'form_var_x1':3  , 'form_var_x2':3 }), 
            ]
        )

    def test_different_string(self):
        self.check('si x1 est différent de "b" alors afficher le message m1', 'm1',
            [
                (True, {'form_var_x1':None }),
                (True, {'form_var_x1':5    }),
                (True, {'form_var_x1':"a"  }), 
                (False, {'form_var_x1':"b"  }), 
            ]
        )

    def test_different_number(self):
        self.check('si x1 est différent de 53 alors afficher le message m1', 'm1',
            [
                (True, {'form_var_x1':None  }),
                (True, {'form_var_x1':3     }),
                (False, {'form_var_x1':53   }),
                (False, {'form_var_x1':"53" }),
                (True, {'form_var_x1':"a"   }), 
            ]
        )

    def test_greater_var(self):
        self.check('si x1 est supérieur à x2 alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None , 'form_var_x2':None}),
                (False, {'form_var_x1':None , 'form_var_x2':"b" }),
                (False, {'form_var_x1':"3" , 'form_var_x2':"b" }),
                (False, {'form_var_x1':"a"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':"b"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':"c"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':"3" , 'form_var_x2':"3" }), 
                (True, {'form_var_x1':"41"  , 'form_var_x2':"4" }), 
                (True, {'form_var_x1':"141"  , 'form_var_x2':"13" }), 
                (False, {'form_var_x1':"32"  , 'form_var_x2':"111" }), 
            ]
        )

    def test_greater_number(self):
        self.check('si x1 est supérieur à 5 alors afficher le message m1', 'm1',
            [
                (True, {'form_var_x1':"6"    }),
                (True, {'form_var_x1':"11"   }),
                (False, {'form_var_x1':"3"   }),
                (False, {'form_var_x1':"5"   }),
                (True, {'form_var_x1':"6"    }),
            ]
        )

    def test_lower_var(self):
        self.check('si x1 est inférieur à x2 alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None , 'form_var_x2':None}),
                (False, {'form_var_x1':None , 'form_var_x2':"b" }),
                (False, {'form_var_x1':"3" , 'form_var_x2':"b" }),
                (False, {'form_var_x1':"a"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':"b"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':"c"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':"3" , 'form_var_x2':"3" }), 
                (False, {'form_var_x1':"41"  , 'form_var_x2':"4" }), 
                (False, {'form_var_x1':"141"  , 'form_var_x2':"13" }), 
                (True, {'form_var_x1':"32"  , 'form_var_x2':"111" }), 
                (True, {'form_var_x1':"2"  , 'form_var_x2':"3" }), 
            ]
        )

    def test_lower_number(self):
        self.check('si x1 est inférieur à 5 alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':"6"    }),
                (False, {'form_var_x1':"11"   }),
                (True, {'form_var_x1':"3"   }),
                (False, {'form_var_x1':"5"   }),
                (False, {'form_var_x1':"6"    }),
            ]
        )

if __name__ == '__main__':
    unittest.main()