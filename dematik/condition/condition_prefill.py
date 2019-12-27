# coding: utf8
from condition import Condition 

# Capture a message in a condition sentence
class ConditionPrefill(Condition):
    
    tokens = [
        ('PYTHON_FORMULA',   r'formule python'),
        ('PRE_FILL',   r'préremplir'),
        ('WITH',   r'avec')
    ]

    sentences = [   
        ('PRE_FILL', 'FIELDNAME', 'WITH', 'PYTHON_FORMULA', 'VALUE'),
        ('PRE_FILL', 'FIELDNAME', 'WITH', 'VALUE'),
        ('PRE_FILL', 'FIELDNAME', 'WITH', 'FIELDNAME'),
    ]

    def __init__(self, sentence_tokens):
        self.type = 'PREFILL'
        self.prefill_fieldname = sentence_tokens[1].value
        if sentence_tokens[3].type == 'PYTHON_FORMULA':
            self.prefill_formula = sentence_tokens[3].value
        else:
            self.prefill_value = sentence_tokens[3].value