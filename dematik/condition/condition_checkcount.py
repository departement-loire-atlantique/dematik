# coding: utf8
from condition import Condition 

class ConditionCheckCount(Condition):

    tokens = [ 
            ('AT_MOST',   r'moins de '),
            ('AT_LEAST',   r'au moins '),
            ('ITEMS_OF',   r'élément[s]? de '),
            ('CHECKED',   r'coché[s]?'),
    ]

    sentences = [ 
            ('AT_LEAST', 'INT_VALUE', 'ITEMS_OF', 'FIELDNAME', 'CHECKED'),
            ('AT_MOST', 'INT_VALUE', 'ITEMS_OF', 'FIELDNAME', 'CHECKED')
    ]

    operator = {
            'AT_LEAST' : '>= ', 
            'AT_MOST' : '< ' 
    }

    def __init__(self, sentence_tokens):
        self.type = "CONDITION"
        self.fieldname = self.protect(sentence_tokens[3].value)
        self.count = sentence_tokens[1].value
        self.op = ConditionCheckCount.operator[sentence_tokens[0].type]
        
    def build(self):
        return self.fieldname + '|default_if_none:""|length ' + self.op + self.count