from condition import Condition 

# Capture a message in a condition sentence
class ConditionMessage(Condition):
    
    tokens = [
        ('THEN',   r'alors'),
        ('PRINT_MESSAGE',   r'afficher le message')
    ]

    sentences = [   
        ('THEN', 'PRINT_MESSAGE', 'FIELDNAME'),
        ('THEN', 'PRINT_MESSAGE', 'VALUE')
    ]

    def __init__(self, sentence_tokens):
        self.type = 'MESSAGE'
        self.message = sentence_tokens[2].value

    def build(self):
        return self.message 