# coding: utf8
from test_condition_parser import ConditionParserTester
import unittest

class ConditionEmptyTest(ConditionParserTester):

    def test_equal(self):
        self.check('si x1 est égal à x2 alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None , 'form_var_x2':None}),
                (False, {'form_var_x1':None , 'form_var_x2':"b" }),
                (False, {'form_var_x1':3 , 'form_var_x2':"b" }),
                (False, {'form_var_x1':"a"  , 'form_var_x2':"b" }), 
                (True, {'form_var_x1':"b"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':2  , 'form_var_x2':3 }), 
                (True, {'form_var_x1':3  , 'form_var_x2':3 }), 
            ]
        )

        self.check('si x1 est égal à "bé" alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None }),
                (False, {'form_var_x1':5    }),
                (False, {'form_var_x1':"a"  }), 
                (True, {'form_var_x1':"b&#233;"  }), 
            ]
        )

        self.check('si x1 est égal à 5 alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None }),
                (False, {'form_var_x1':3    }),
                (True, {'form_var_x1':5    }),
                (False, {'form_var_x1':"a"  }), 
            ]
        )

    def test_different(self):
        self.check('si x1 est différent de x2 alors afficher le message m1', 'm1',
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

        self.check('si x1 est différent de "b" alors afficher le message m1', 'm1',
            [
                (True, {'form_var_x1':None }),
                (True, {'form_var_x1':5    }),
                (True, {'form_var_x1':"a"  }), 
                (False, {'form_var_x1':"b"  }), 
            ]
        )

        self.check('si x1 est différent de 5 alors afficher le message m1', 'm1',
            [
                (True, {'form_var_x1':None }),
                (True, {'form_var_x1':3    }),
                (False, {'form_var_x1':5    }),
                (True, {'form_var_x1':"a"  }), 
            ]
        )

    def test_greater(self):
        self.check('si x1 est supérieur à x2 alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None , 'form_var_x2':None}),
                (False, {'form_var_x1':None , 'form_var_x2':"b" }),
                (False, {'form_var_x1':3 , 'form_var_x2':"b" }),
                (False, {'form_var_x1':"a"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':"b"  , 'form_var_x2':"b" }), 
                (True, {'form_var_x1':"c"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':3  , 'form_var_x2':3 }), 
                (True, {'form_var_x1':4  , 'form_var_x2':3 }), 
                (False, {'form_var_x1':2  , 'form_var_x2':3 }), 
            ]
        )

        self.check('si x1 est supérieur à "b" alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None }),
                (False, {'form_var_x1':5    }),
                (False, {'form_var_x1':"b"  }), 
                (True, {'form_var_x1':"c"  }), 
            ]
        )

        self.check('si x1 est supérieur à 5 alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None }),
                (False, {'form_var_x1':3    }),
                (False, {'form_var_x1':5    }),
                (True, {'form_var_x1':6    }),
                (False, {'form_var_x1':"a"  }), 
            ]
        )

    def test_lower(self):
        self.check('si x1 est inférieur à x2 alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None , 'form_var_x2':None}),
                (False, {'form_var_x1':None , 'form_var_x2':"b" }),
                (False, {'form_var_x1':3 , 'form_var_x2':"b" }),
                (True, {'form_var_x1':"a"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':"b"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':"c"  , 'form_var_x2':"b" }), 
                (False, {'form_var_x1':3  , 'form_var_x2':3 }), 
                (False, {'form_var_x1':4  , 'form_var_x2':3 }), 
                (True, {'form_var_x1':2  , 'form_var_x2':3 }), 
            ]
        )

        self.check('si x1 est inférieur à "b" alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None }),
                (False, {'form_var_x1':5    }),
                (True, {'form_var_x1':"a"  }), 
                (False, {'form_var_x1':"c"  }), 
            ]
        )

        self.check('si x1 est inférieur à 5 alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None }),
                (True, {'form_var_x1':3    }),
                (False, {'form_var_x1':5    }),
                (False, {'form_var_x1':6    }),
                (False, {'form_var_x1':"a"  }), 
            ]
        )

if __name__ == '__main__':
    unittest.main()