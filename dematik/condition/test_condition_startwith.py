# coding: utf8
from test_condition_parser import ConditionParserTester
import unittest

class ConditionStartWithTest(ConditionParserTester):

    def test_startwith(self):
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

    def test_notstartwith(self):
        self.check('si x1 ne commence pas par "44" alors afficher le message m1', 'm1',
            [
                (True, {'form_var_x1': None    }),
                (True, {'form_var_x1': []      }),
                (True, {'form_var_x1': ""      }),
                (True, {'form_var_x1': "a"     }),
                (True, {'form_var_x1': ['e']   }),
                (True, {'form_var_x1': "a44a"  }),
                (True, {'form_var_x1': "a44"   }),
                (False, {'form_var_x1': "44"    }),
                (False,  {'form_var_x1': "44a"   }),
            ]
        )


if __name__ == '__main__':
    unittest.main()