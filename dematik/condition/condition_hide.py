from condition import Condition 

# Capture a message in a condition sentence
class ConditionHide(Condition):
    
    tokens = [
        ('HIDE_PAGE',   r'masquer cette page'),
        ('HIDE_FIELD',   r'masquer le champ')
    ]

    sentences = [   
        ('THEN', 'HIDE_PAGE'),
        ('THEN', 'HIDE_FIELD', 'FIELDNAME')
    ]

    def __init__(self, sentence_tokens):
        if sentence_tokens[1].type == 'HIDE_PAGE':
            self.type = 'HIDE_PAGE'
        else:
            self.type = 'HIDE_FIELD'
            self.hidden_fieldname = sentence_tokens[2].value
