# coding: utf8
from condition import Condition 

class ConditionCompare(Condition):

    tokens = [ 
        ('DIFFERENT',   r'différent de'),
        ('EQUAL',   r'égal à'),
        ('GREATER',   r'supérieur à'),
        ('LOWER',   r'inférieur à')
    ]

    sentences = [ 
        ('FIELDNAME', 'DIFFERENT', 'FIELDNAME'), 
        ('FIELDNAME', 'DIFFERENT', 'VALUE'),
        ('FIELDNAME', 'DIFFERENT', 'INT_VALUE'),

        ('FIELDNAME', 'EQUAL', 'FIELDNAME'), 
        ('FIELDNAME', 'EQUAL', 'VALUE'),
        ('FIELDNAME', 'EQUAL', 'INT_VALUE'),

        ('FIELDNAME', 'GREATER', 'FIELDNAME'), 
        ('FIELDNAME', 'GREATER', 'VALUE'),
        ('FIELDNAME', 'GREATER', 'INT_VALUE'),

        ('FIELDNAME', 'LOWER', 'FIELDNAME'), 
        ('FIELDNAME', 'LOWER', 'VALUE'),
        ('FIELDNAME', 'LOWER', 'INT_VALUE'),
    ]

    operators = {
        'EQUAL':'==', 
        'GREATER':'>', 
        'LOWER':'<', 
        'DIFFERENT':'!='
    }

    def __init__(self, sentence_tokens):
        self.type = "CONDITION"
        
        self.field = self.protect(sentence_tokens[0].value)

        self.operator = ConditionCompare.operators[sentence_tokens[1].type]

        if sentence_tokens[2].type == 'FIELDNAME':
            self.operand = self.protect(sentence_tokens[2].value)
        else:
            self.operand = sentence_tokens[2].value

    def build(self):   
        if self.operator == '!=':
            return self.field + self.operator + self.operand + ' if isinstance(' + self.field + ', (' + self.operand + ').__class__) else True'
        else:    
            return self.field + self.operator + self.operand + ' if ' + self.field + ' and isinstance(' + self.field + ', (' + self.operand + ').__class__) else False'