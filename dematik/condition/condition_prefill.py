# coding: utf8
from condition import Condition 

# Capture a message in a condition sentence
class ConditionPrefill(Condition):
    
    tokens = [
        ('PRE_FILL',   r'préremplir'),
        ('WITH',   r'avec')
    ]

    sentences = [   
        ('THEN', 'PREFILL'),
        ('PRE_FILL', 'FIELDNAME', 'WITH', 'VALUE'),
        ('PRE_FILL', 'FIELDNAME', 'WITH', 'FIELDNAME'),
    ]

    def __init__(self, sentence_tokens):
        self.type = 'PREFILL'
        if sentence_tokens[0].type == 'THEN':
            self.prefill_fieldname = sentence_tokens[1].value.prefill_fieldname
            self.prefill_value = sentence_tokens[1].value.prefill_value
        else:
            self.prefill_fieldname = sentence_tokens[1].value
            self.prefill_value = sentence_tokens[3].value