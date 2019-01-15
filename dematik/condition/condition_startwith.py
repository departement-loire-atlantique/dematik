# coding: utf8
from condition import Condition 

class ConditionStartWith(Condition):

    tokens = [ 
           ('STARTWITH',   r'commence par'),
        ]

    sentences = [ 
           ('FIELDNAME', 'STARTWITH', 'VALUE'), 
    ]

    def __init__(self, sentence_tokens):
        self.type = 'CONDITION'

        self.field = sentence_tokens[0].value
        self.operand = sentence_tokens[2].value
            
    def build(self, language):
        field = self.protect(self.field, language)

        if language == 'python':
            isstr = ' if ' + field + ' and isinstance(' + field + ', str) else False'
            return field + '.startswith(' + self.operand + ')' + isstr
        
        elif language == 'django':
            s_op = str(len(self.operand)-2)
            return field + "|make_list|slice:':" + s_op + ":'|join:'' == " + self.operand

        else:
            raise('not implemented')