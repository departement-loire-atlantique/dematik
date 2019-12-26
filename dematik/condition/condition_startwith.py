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

        self.field = self.protect(sentence_tokens[0].value)
        self.op = '==' if sentence_tokens[1].type == 'STARTWITH' else '!='
        self.operand = sentence_tokens[2].value
            
    def build(self):
        s_op = str(len(self.operand)-2)
        return self.field + "|make_list|slice:':" + s_op + ":'|join:'' " + self.op + " " + self.operand