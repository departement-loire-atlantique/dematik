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
        'EQUAL':' == ', 
        'GREATER':' > ', 
        'LOWER':' < ', 
        'DIFFERENT':' != '
    }

    def __init__(self, sentence_tokens):
        self.type = "CONDITION"
        
        self.field = sentence_tokens[0].value
        self.operator = ConditionCompare.operators[sentence_tokens[1].type]  
        self.operand = sentence_tokens[2]

    def build(self, language):   
        operand = self.protect(self.operand.value, language) if self.operand.type == 'FIELDNAME' else self.operand.value
        field = self.protect(self.field, language)

        if language == 'python':
            return '(' + field + ' if ' + field + ' and isinstance(' + field + ', (' + operand + ').__class__) else "")' + self.operator + '(' + operand + ' if ' + operand + ' else "")'
        
        elif language == 'django':
            return field + '|default_if_none:""' + self.operator + operand + '|default_if_none:""'
          
        else:
            raise('not implemented')