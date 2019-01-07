from condition import Condition 

class ConditionOperator(Condition):
    
    tokens = [ 
        ('OR',   r'ou'),
        ('AND',   r'et'), 
    ]
    
    sentences = [ 
        ('CONDITION', 'AND', 'CONDITION'), 
        ('CONDITION', 'OR', 'CONDITION')
    ]

    def __init__(self, sentence_tokens):
        self.type = "CONDITION"
       
        self.left_condition = sentence_tokens[0].value
        self.operator = sentence_tokens[1].type.lower()
        self.right_condition = sentence_tokens[2].value

    def build(self, language):
        return '(' + self.left_condition.build(language) + ') ' + self.operator + ' (' + self.right_condition.build(language) + ')'