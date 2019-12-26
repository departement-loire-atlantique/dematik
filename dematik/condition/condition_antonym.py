# coding: utf8
from condition import Condition 

class ConditionAntonym(Condition):
    
    tokens = [
            ('NOT',   r'n\'est pas'),
    ]
    
    sentences = [ 
            ('NOT', 'EMPTY'),
            ('NOT', 'EQUAL'),
            ('NOT', 'FILLED'),
            ('NOT', 'CHECKED'),
    ]

    antonym = {
            'EMPTY'   : 'FILLED',
            'EQUAL'   : 'DIFFERENT',
            'FILLED'  : 'EMPTY',
            'CHECKED' : 'EMPTY',
    }

    def __init__(self, sentence_tokens):
        self.type = self.antonym[sentence_tokens[1].type]

    def build(self):
        return self.type