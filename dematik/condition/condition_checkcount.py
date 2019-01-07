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
            'AT_LEAST' : '>=', 
            'AT_MOST' : '<' 
    }

    def __init__(self, sentence_tokens):
        self.type = "CONDITION"
        
        self.fieldname = sentence_tokens[3].value
        self.count = sentence_tokens[1].value
        self.op = ConditionCheckCount.operator[sentence_tokens[0].type]
        
    def build(self, language):
        if language == 'python':
            return 'len(' + self.protect_as_list(self.fieldname, language) +')' + self.op + self.count
        elif language == 'django':
            field =  self.protect(self.fieldname, language)
            return '((' + field + ' is none and 0' + self.op + self.count + ') or (' + field + '|length' + self.op + self.count + '))'
        else:
            raise Exception("not implemented")