# coding: utf8
import re
import importlib
from os import listdir
from os.path import isfile, join, realpath, dirname
from dematik.field_data import FieldData

# Import and declare all conditions
from condition import Condition
from condition_antonym import ConditionAntonym
from condition_checkcount import ConditionCheckCount
from condition_compare import ConditionCompare
from condition_filled import ConditionFilled
from condition_hide import ConditionHide
from condition_message import ConditionMessage
from condition_operator import ConditionOperator
from condition_string import ConditionString
from condition_startwith import ConditionStartWith
from condition_token import Token

condition_classes = [
    Condition,
    ConditionAntonym,
    ConditionCheckCount,
    ConditionCompare,
    ConditionFilled,
    ConditionHide,
    ConditionMessage,
    ConditionOperator,
    ConditionString,
    ConditionStartWith,
]

# ConditionParser allows to parse a condition as "french text" and
# build a valid python condition from it
class ConditionParser:

    # Transform a text in a list of Token
    def tokenize(self, condition_as_text):

        token_specification = []
        fd = FieldData()
        
        # Add specific tokens
        for condition_class in condition_classes:
            token_specification += condition_class.tokens

        # Global tokens
        token_specification += [
            ('IF_STOP_WORD',   r'si'),      # Ignored
            ('IS_STOP_WORD',   r'est'),     # Ignored
            ('ARE_STOP_WORD',   r'sont'),   # Ignored
            ('INT_VALUE', r'\d+'),
            ('VALUE', r'".*"'),
            ('FIELDNAME', r'\w*:?\w+'),
        ]

        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
   
        last_token =  Token("", "", False)
        for mo in re.finditer(tok_regex, condition_as_text):
            kind = mo.lastgroup
            value = mo.group()

            # UTF-8 for VALUE
            if kind == 'VALUE':
                value = '"%s"' % fd.htmlescape(value[1:-1].decode('utf-8'))

            # Adjacent tokens can't be all FIELDNAME
            if kind == 'FIELDNAME' and last_token.type == 'FIELDNAME':
                unknowns = (last_token.value, value)
                raise Exception("Un des termes suivants n'est pas encore supporté dans les conditions : %s" % ' ou '.join(unknowns))
           
            # Namepace support
            if kind == 'FIELDNAME':
                value = value.replace(':', '_')

            # Ignore stop words
            if not 'STOP_WORD' in kind :
                last_token = Token(kind, value, False)
                yield last_token

    # Transform a text in a Condition or raise and Exception 
    def parse(self, text):
        clean_text = ' '.join(text.split())
        tokens = [token for token in self.tokenize(clean_text) ]
        
        # Merge tokens until nothing could be merged anymore
        last_token_count = len(tokens) + 1
        while(last_token_count > len(tokens)):
            last_token_count = len(tokens)
            for condition_class in condition_classes:
                tokens = self.merge_using_condition(condition_class, tokens)

        if len(tokens) != 1:
            unknowns = [token.value + '(' + token.type + ')' for token in tokens if not token.merged]
            if unknowns: 
                raise Exception("Les termes suivants ne sont pas encore supportés dans les conditions : %s" % ', '.join(unknowns))
            else:
                for token in tokens:
                    print(token)
                raise Exception("La phrase n'est pas supportée")
        
        return tokens[0].value

    # Merge tokens using a condition
    def merge_using_condition(self, condition_class, tokens):
        sentences = condition_class.sentences
        for sentence in sentences:
            sentence_index = 0

            for i, token in enumerate(tokens):
                if token.type == sentence[sentence_index]:
                    sentence_index = sentence_index + 1
                    if len(sentence) == sentence_index:
                        # A valid sentense for this condition match => Merge
                        c = condition_class(tokens[i-sentence_index+1:i+1])
                        condition_token = [Token(type=c.getType(), value=c, merged=True)]
                        return tokens[:i-sentence_index+1] + condition_token + tokens[i+1:]
                else:
                   sentence_index = 0
        
        # No any sentense for this condition match => Do nothing
        return tokens