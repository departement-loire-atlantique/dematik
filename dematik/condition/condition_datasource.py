# coding: utf8
from condition import Condition 

# Capture a message in a condition sentence
class ConditionDatasource(Condition):
    
    tokens = [
        ('LINK_FIELD',   r'lier le champ'),
        ('PYTHON_EXPRESSION',   r'les choix issus de l\'expression python'),
        ('DATASOURCE',   r'la source de données'),
        ('NAMED',   r'nommée'),
        ('JSONP',   r'jsonp'),
        ('JSON',   r'json'),
    ]

    sentences = [   
        ('LINK_FIELD', 'FIELDNAME', 'WITH', 'PYTHON_EXPRESSION', 'VALUE'),
        ('LINK_FIELD', 'FIELDNAME', 'WITH', 'DATASOURCE', 'NAMED', 'VALUE'),
        ('LINK_FIELD', 'FIELDNAME', 'WITH', 'DATASOURCE', 'JSON', 'VALUE'),
        ('LINK_FIELD', 'FIELDNAME', 'WITH', 'DATASOURCE', 'JSONP', 'VALUE'),
        ('LINK_FIELD', 'FIELDNAME', 'WITH', 'DATASOURCE', 'NAMED', 'FIELDNAME'),
        ('LINK_FIELD', 'FIELDNAME', 'WITH', 'DATASOURCE', 'JSON', 'FIELDNAME'),
        ('LINK_FIELD', 'FIELDNAME', 'WITH', 'DATASOURCE', 'JSONP', 'FIELDNAME'),
    ]

    transcode = {
        'PYTHON_EXPRESSION' : 'formula',
        'JSONP' : 'jsonp',
        'JSON' : 'json',
    }

    def __init__(self, sentence_tokens):
        self.type = 'DATASOURCE'
        self.datasource_fieldname = sentence_tokens[1].value
        if sentence_tokens[3].type == 'PYTHON_EXPRESSION':
            self.datasource_type = ConditionDatasource.transcode[sentence_tokens[3].type]
            self.datasource_value = sentence_tokens[4].value
        elif sentence_tokens[4].type == 'NAMED':
            self.datasource_type = sentence_tokens[5].value #[1:-1] if sentence_tokens[5].type == 'VALUE' else sentence_tokens[5].value
        else:
            self.datasource_type = ConditionDatasource.transcode[sentence_tokens[4].type]
            self.datasource_value = sentence_tokens[5].value #[1:-1] if sentence_tokens[5].type == 'VALUE' else sentence_tokens[5].value