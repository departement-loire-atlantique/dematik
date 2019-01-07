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
        self.fieldname = sentence_tokens[0].value   
        if sentence_tokens[1].type == 'EMPTY':
            self.op = '== 0'
        else:
            self.op = '> 0'

    def build(self, language):
        
        if language == 'python':
            return 'len(' + self.protect_as_list(self.fieldname,language) +')' + self.op
        elif language == 'django':
            field = self.protect(self.fieldname, language)
            if "== 0" in self.op:
                return '(' + field + ' is none or ' + field + '|length' + self.op + ')'
            else:
                return '(' + field + ' is not none and ' + field + '|length' + self.op + ')'
        else:
            raise Exception("not implemented")