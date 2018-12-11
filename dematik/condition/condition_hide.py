from condition import Condition 

# Capture a message in a condition sentence
class ConditionHide(Condition):
    
    tokens = [
        ('HIDE_PAGE',   r'masquer cette page')
    ]

    sentences = [   
        ('THEN', 'HIDE_PAGE')
    ]

    def __init__(self, sentence_tokens):
        self.type = 'HIDE_PAGE'