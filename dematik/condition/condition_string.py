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

        self.field = self.protect(sentence_tokens[0].value)
        self.op = ConditionString.operators[sentence_tokens[1].type]
        self.operand = self.protect(sentence_tokens[2].value) if sentence_tokens[2].type == 'FIELDNAME' else sentence_tokens[2].value
            
    def build(self):
        return self.operand + '|default_if_none:""|stringformat:"s"' + self.op[0] + self.field + '|default_if_none:""|stringformat:"s" ' + self.op[1]