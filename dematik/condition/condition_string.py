# coding: utf8
from condition import Condition 

class ConditionString(Condition):

    tokens = [ 
            ('NOT_CONTAINS',   r'ne contient pas'),
            ('CONTAINS',   r'contient '),
        ]

    sentences = [ 
            ('FIELDNAME', 'NOT_CONTAINS', 'FIELDNAME'), 
            ('FIELDNAME', 'NOT_CONTAINS', 'VALUE'), 

            ('FIELDNAME', 'CONTAINS', 'FIELDNAME'), 
            ('FIELDNAME', 'CONTAINS', 'VALUE'), 
    ]

    operators = {
            'NOT_CONTAINS': (' not in ', '', 'True'),
            'CONTAINS': (' in ', '', 'False')
    }

    def __init__(self, sentence_tokens):
        self.type = 'CONDITION'

        self.field = sentence_tokens[0].value
        self.op = ConditionString.operators[sentence_tokens[1].type]
        self.operand = sentence_tokens[2]
            
    def build(self, language):
        operand = self.protect(self.operand.value, language) if self.operand.type == 'FIELDNAME' else self.operand.value
        field = self.protect(self.field, language)

        if language == 'python':
            isstr = ' if ' + field + ' and isinstance(' + field + ', str) else '+ self.op[2]
            return operand + self.op[0] + field + self.op[1] + isstr
        
        elif language == 'django':
            if "not" in self.op[0]:
                return '(' + field + ' is none or ' + operand + '|string' + self.op[0] + field + '|string' + self.op[1] + ')'
            else:
                return '(' + field + ' is not none and ' + operand + '|string' + self.op[0] + field + '|string' + self.op[1] + ')'

        else:
            raise('not implemented')