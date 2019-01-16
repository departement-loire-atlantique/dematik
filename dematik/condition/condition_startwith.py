# coding: utf8
from condition import Condition 

class ConditionStartWith(Condition):

    tokens = [ 
           ('STARTWITH',   r'commence par'),
           ('NOT_STARTWITH',   r'ne commence pas par'),
        ]

    sentences = [ 
           ('FIELDNAME', 'STARTWITH', 'VALUE'),
           ('FIELDNAME', 'NOT_STARTWITH', 'VALUE'),
    ]

    def __init__(self, sentence_tokens):
        self.type = 'CONDITION'

        self.field = sentence_tokens[0].value
        self.subtype = sentence_tokens[1].type
        self.operand = sentence_tokens[2].value
            
    def build(self, language):
        field = self.protect(self.field, language)

        if language == 'python':
            isstr = ' if ' + field + ' and isinstance(' + field + ', str) else False'
            isnot = 'not (' if self.subtype == 'NOT_STARTWITH' else '('
            return isnot + field + '.startswith(' + self.operand + ')' + isstr + ')'
        
        elif language == 'django':
            s_op = str(len(self.operand)-2)
            equals_or_not_equals = '==' if self.subtype == 'STARTWITH' else '!='
            return field + "|make_list|slice:':" + s_op + ":'|join:'' " + equals_or_not_equals + " " + self.operand

        else:
            raise('not implemented')