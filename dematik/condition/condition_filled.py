# coding: utf8
from condition import Condition 

class ConditionFilled(Condition):
    
    tokens = [
        ('EMPTY',   r'vide'),
        ('FILLED',   r'rempli '),
    ]
    
    sentences = [ 
        ('FIELDNAME', 'EMPTY'), 
        ('FIELDNAME', 'FILLED'),
        ('FIELDNAME', 'CHECKED'),
    ]

    def __init__(self, sentence_tokens):
        self.type = "CONDITION"
        fieldname = self.protect(sentence_tokens[0].value)
        if sentence_tokens[1].type == 'EMPTY':
            self.cond = fieldname + '|default_if_none:""|length == 0'
        else:
            self.cond =  fieldname + '|default_if_none:""|length > 0'

    def build(self):
        return self.cond