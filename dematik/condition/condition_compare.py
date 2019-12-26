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
        ('FIELDNAME', 'GREATER', 'INT_VALUE'),

        ('FIELDNAME', 'LOWER', 'FIELDNAME'), 
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
        
        self.field = self.protect(sentence_tokens[0].value)
        self.operator = ConditionCompare.operators[sentence_tokens[1].type]  
        self.operand = sentence_tokens[2]

    def build(self):   
        operand = self.protect(self.operand.value) if self.operand.type == 'FIELDNAME' else self.operand.value
        
        if self.operand.type == 'INT_VALUE':
            return self.field + '|default_if_none:""|add:"0"' + self.operator + operand
        elif '>' in self.operator :
            # Field :   None    -> none     -> none0    -> ""       -> "-10000000"  -> -10000000
            # Operand : None    -> none     -> none0    -> ""       -> "10000000"   -> 10000000
            # Field :   "a"     -> "a"      -> "a0"     -> ""       -> "-10000000"  -> -10000000
            # Operand : "a"     -> "a"      -> "a0"     -> ""       -> "10000000"   -> 10000000
            # Field :   "1"     -> "1"      -> 1        -> 1        -> 1            -> 1 
            # Operand : "1"     -> "1"      -> 1        -> 1        -> 1            -> 1 
            return self.field + '|default_if_none:"none"|add:"0"|stringformat:"d"|default:"-10000000"|add:"0"' + self.operator + operand + '|default_if_none:"none"|add:"0"|stringformat:"d"|default:"10000000"|add:"0"'
        elif '<' in self.operator :
            return self.field + '|default_if_none:"none"|add:"0"|stringformat:"d"|default:"10000000"|add:"0"' + self.operator + operand + '|default_if_none:"none"|add:"0"|stringformat:"d"|default:"-10000000"|add:"0"'
        else:
            return self.field + '|default_if_none:""' + self.operator + operand + '|default_if_none:""'