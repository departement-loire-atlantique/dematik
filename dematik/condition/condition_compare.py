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
        
        self.field = sentence_tokens[0].value
        self.operator = ConditionCompare.operators[sentence_tokens[1].type]  
        self.operand = sentence_tokens[2]

    def build(self, language):   
        operand = self.protect(self.operand.value, language) if self.operand.type == 'FIELDNAME' else self.operand.value
        field = self.protect(self.field, language)

        if language == 'python':
            default = str(self.operator == ' != ')
            if self.operand.type == 'INT_VALUE':
                return 'int(' + field + ')' + self.operator + operand + ' if ' + field + ' and (isinstance(' + field + ', int) or (isinstance(' + field + ', str) and ' + field + '.isdigit())) else ' + default
            elif '>' in self.operator or '<' in self.operator :
                return 'int(' + field + ')' + self.operator + 'int(' + operand + ') ' \
                        + 'if ' + field + ' and (isinstance(' + field + ', int) or (isinstance(' + field + ', str) and ' + field + '.isdigit())) ' \
                        +    'and ' + operand + ' and (isinstance(' + operand + ', int) or (isinstance(' + operand + ', str) and ' + operand + '.isdigit())) ' \
                        + ' else ' + default
            else:
                return '(' + field + ' if ' + field + ' and isinstance(' + field + ', (' + operand + ').__class__) else "")' + self.operator + '(' + operand + ' if ' + operand + ' else "")'
        
        elif language == 'django':
            if self.operand.type == 'INT_VALUE':
                return field + '|default_if_none:""|add:"0"' + self.operator + operand
            elif '>' in self.operator :
                # Field :   None    -> none     -> none0    -> ""       -> "-10000000"  -> -10000000
                # Operand : None    -> none     -> none0    -> ""       -> "10000000"   -> 10000000
                # Field :   "a"     -> "a"      -> "a0"     -> ""       -> "-10000000"  -> -10000000
                # Operand : "a"     -> "a"      -> "a0"     -> ""       -> "10000000"   -> 10000000
                # Field :   "1"     -> "1"      -> 1        -> 1        -> 1            -> 1 
                # Operand : "1"     -> "1"      -> 1        -> 1        -> 1            -> 1 
                return field + '|default_if_none:"none"|add:"0"|stringformat:"d"|default:"-10000000"|add:"0"' + self.operator + operand + '|default_if_none:"none"|add:"0"|stringformat:"d"|default:"10000000"|add:"0"'
            elif '<' in self.operator :
                return field + '|default_if_none:"none"|add:"0"|stringformat:"d"|default:"10000000"|add:"0"' + self.operator + operand + '|default_if_none:"none"|add:"0"|stringformat:"d"|default:"-10000000"|add:"0"'
            else:
                return field + '|default_if_none:""' + self.operator + operand + '|default_if_none:""'
          
        else:
            raise('not implemented')