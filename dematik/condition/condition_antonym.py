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

    def __init__(self, sentence_tokens):
        if sentence_tokens[1].type == 'EMPTY':
            self.type = 'FILLED'

        if sentence_tokens[1].type == 'EQUAL':
            self.type = 'DIFFERENT'

        if sentence_tokens[1].type == 'FILLED' or sentence_tokens[1].type == 'CHECKED':
            self.type = 'EMPTY'
    
    def build(self):
        return self.type