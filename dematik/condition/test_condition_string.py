# coding: utf8
from test_condition_parser import ConditionParserTester
import unittest

class ConditionStringTest(ConditionParserTester):

    def test_start_with(self):

        self.check('si x1 commence par "44" alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1': None    }),
                (False, {'form_var_x1': []      }),
                (False, {'form_var_x1': ""      }),
                (False, {'form_var_x1': "a"     }),
                (False, {'form_var_x1': ['e']   }),
                (False, {'form_var_x1': "a44a"  }),
                (False, {'form_var_x1': "a44"   }),
                (True, {'form_var_x1': "44"    }),
                (True,  {'form_var_x1': "44a"   }),
            ]
        )

        self.check('si x1 commence par x2 alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None , 'form_var_x2':None }),
                (False, {'form_var_x1':None , 'form_var_x2':"b"  }),
                (False, {'form_var_x1':3    , 'form_var_x2':"b"  }),
                (False, {'form_var_x1':3    , 'form_var_x2':3    }), 
                (False, {'form_var_x1':"a"  , 'form_var_x2':"b"  }), 
                (False, {'form_var_x1':"ba" , 'form_var_x2':"a"  }),
                (True, {'form_var_x1':"ab" , 'form_var_x2':"a" }),
                (True, {'form_var_x1':"abc " , 'form_var_x2':"ab" }), 
            ]
        )
        
    def test_not_start_with(self):

        self.check('si x1 ne commence pas par "44" alors afficher le message m1', 'm1',
            [
                (True,  {'form_var_x1': None    }),
                (True,  {'form_var_x1': []      }),
                (True,  {'form_var_x1': ""      }),
                (True,  {'form_var_x1': "a"     }),
                (True,  {'form_var_x1': ['e']   }),
                (True,  {'form_var_x1': "a44a"  }),
                (True,  {'form_var_x1': "a44"   }),
                (False,  {'form_var_x1': "44"    }),
                (False, {'form_var_x1': "44a"   }),
            ]
        )
        
        self.check('si x1 ne commence pas par x2 alors afficher le message m1', 'm1',
            [
                (True, {'form_var_x1':None , 'form_var_x2':None }),
                (True, {'form_var_x1':None , 'form_var_x2':"b"  }),
                (True, {'form_var_x1':3    , 'form_var_x2':"b"  }),
                (True, {'form_var_x1':3    , 'form_var_x2':3    }), 
                (True, {'form_var_x1':"a"  , 'form_var_x2':"b"  }), 
                (True, {'form_var_x1':"ba" , 'form_var_x2':"a"  }),
                (False, {'form_var_x1':"ab" , 'form_var_x2':"a" }),
                (False, {'form_var_x1':"abc " , 'form_var_x2':"ab" }), 
            ]
        )

    def test_contains(self):
        self.check('si x1 contient "44" alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1': None    }),
                (False, {'form_var_x1': []      }),
                (False, {'form_var_x1': ""      }),
                (False, {'form_var_x1': "a"     }),
                (False, {'form_var_x1': ['e']   }),
                (True, {'form_var_x1': "a44a"  }),
                (True, {'form_var_x1': "a44"   }),
                (True, {'form_var_x1': "44"    }),
                (False,  {'form_var_x1': "4a"   }),
            ]
        )

        self.check('si x1 contient x2 alors afficher le message m1', 'm1',
            [
                (False, {'form_var_x1':None , 'form_var_x2':None }),
                (False, {'form_var_x1':None , 'form_var_x2':"b"  }),
                (False, {'form_var_x1':3    , 'form_var_x2':"b"  }),
                (False, {'form_var_x1':3    , 'form_var_x2':3    }), 
                (False, {'form_var_x1':"a"  , 'form_var_x2':"b"  }), 
                (True, {'form_var_x1':"ba" , 'form_var_x2':"a"  }),
                (True, {'form_var_x1':"ab" , 'form_var_x2':"a" }),
                (True, {'form_var_x1':"abc " , 'form_var_x2':"ab" }), 
            ]
        )

    def test_not_contains(self):
        self.check('si x1 ne contient pas "44" alors afficher le message m1', 'm1',
            [
                (True,  {'form_var_x1': None    }),
                (True,  {'form_var_x1': []      }),
                (True,  {'form_var_x1': ""      }),
                (True,  {'form_var_x1': "a"     }),
                (True,  {'form_var_x1': ['e']   }),
                (False,  {'form_var_x1': "a44a"  }),
                (False,  {'form_var_x1': "a44"   }),
                (False,  {'form_var_x1': "44"    }),
                (False, {'form_var_x1': "44a"   }),
            ]
        )
        
        self.check('si x1 ne contient pas x2 alors afficher le message m1', 'm1',
            [
                (True, {'form_var_x1':None , 'form_var_x2':None }),
                (True, {'form_var_x1':None , 'form_var_x2':"b"  }),
                (True, {'form_var_x1':3    , 'form_var_x2':"b"  }),
                (True, {'form_var_x1':3    , 'form_var_x2':3    }), 
                (True, {'form_var_x1':"a"  , 'form_var_x2':"b"  }), 
                (False, {'form_var_x1':"ba" , 'form_var_x2':"a"  }),
                (False, {'form_var_x1':"ab" , 'form_var_x2':"a" }),
                (False, {'form_var_x1':"abc " , 'form_var_x2':"ab" }), 
            ]
        )


if __name__ == '__main__':
    unittest.main()