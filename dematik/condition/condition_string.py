# coding: utf8
from condition import Condition 

class ConditionString(Condition):

    tokens = [ 
            ('NOT_STARTWITH',   r'ne commence pas par'),
            ('STARTWITH',   r'commence par'),
            ('NOT_CONTAINS',   r'ne contient pas'),
            ('CONTAINS',   r'contient '),
        ]

    sentences = [ 
            ('FIELDNAME', 'NOT_STARTWITH', 'FIELDNAME'), 
            ('FIELDNAME', 'NOT_STARTWITH', 'VALUE'), 

            ('FIELDNAME', 'STARTWITH', 'FIELDNAME'), 
            ('FIELDNAME', 'STARTWITH', 'VALUE'), 

            ('FIELDNAME', 'NOT_CONTAINS', 'FIELDNAME'), 
            ('FIELDNAME', 'NOT_CONTAINS', 'VALUE'), 

            ('FIELDNAME', 'CONTAINS', 'FIELDNAME'), 
            ('FIELDNAME', 'CONTAINS', 'VALUE'), 
    ]

    operators = {
            'NOT_STARTWITH': ('not ', '.startswith(', ')', 'True'),
            'STARTWITH': ('', '.startswith(', ')', 'False'),
            'NOT_CONTAINS': ('', ' not in ', '', 'True'),
            'CONTAINS': ('', ' in ', '', 'False')
    }

    def __init__(self, sentence_tokens):
        self.type = 'CONDITION'

        self.field = self.protect(sentence_tokens[0].value)
        self.op = ConditionString.operators[sentence_tokens[1].type]
        if sentence_tokens[2].type == 'FIELDNAME':
            self.operand = self.protect(sentence_tokens[2].value)
        else:
            self.operand = sentence_tokens[2].value
            
    def build(self):
        isstr = ' if ' + self.field + ' and isinstance(' + self.field + ', str) else '+ self.op[3]

        if 'in' in self.op[1]:
            return self.op[0] + self.operand + self.op[1] + self.field + self.op[2] + isstr
        else:
            return self.op[0] + self.field + self.op[1] + self.operand + self.op[2] + isstr