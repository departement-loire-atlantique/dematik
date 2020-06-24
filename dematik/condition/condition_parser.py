# coding: utf8
import re
import importlib
from os import listdir
from os.path import isfile, join, realpath, dirname
from field_data import FieldData

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
from condition_prefill import ConditionPrefill
from condition_datasource import ConditionDatasource
from condition_token import Token

condition_classes = [
    ConditionAntonym,
    ConditionCheckCount,
    ConditionFilled,
    ConditionCompare,
    Condition,
    ConditionString,
    ConditionStartWith,
    ConditionOperator,
    ConditionHide,
    ConditionMessage,
    ConditionPrefill,
    ConditionDatasource,
]

# ConditionParser allows to parse a condition as "french text" and
# build a valid django expression
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
            ('VALUE', r'"(.+?)"'),
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
                raise Exception("Un des termes suivants n'est pas encore supporté dans les conditions : %s" % ' ou '.join([last_token.value, value]))
           
            # Namepace support
            if kind == 'FIELDNAME':
                value = value.replace(':', '___')

            # Ignore stop words
            if not 'STOP_WORD' in kind :
                last_token = Token(kind, value, False)
                yield last_token

    # Transform a text in a Condition or raise and Exception 
    def parse(self, text):
        clean_text = ' '.join(text.split())
        tokens = [token for token in self.tokenize(clean_text) ]
        # print("********************************")
        # print(tokens)
        
        # Merge tokens until nothing could be merged anymore
        last_token_count = len(tokens) + 1
        while(last_token_count > len(tokens)):
            last_token_count = len(tokens)
            for condition_class in condition_classes:
                new_merge = True
                while new_merge :
                    tokens,new_merge = self.merge_using_condition(condition_class, tokens)
                    # print("-------")
                    # print(condition_class)
                    # print(tokens)
                    # print("-------")

        if len(tokens) != 1:
            unknowns = [token.value + '(' + token.type + ')' for token in tokens if not token.merged]
            if unknowns: 
                # for t in tokens:
                    # print(t.type, t.value)
                    # print("----")
                raise Exception("Les termes suivants ne sont pas encore supportés dans les conditions : %s" % ', '.join(unknowns))
            else:
                # for token in tokens:
                    # print(token)
                raise Exception("La phrase n'est pas supportée")
        # print(tokens[0])
        # print("********************************")
        
        return tokens[0].value

    # Merge tokens using a condition
    def merge_using_condition(self, condition_class, tokens):
        sentences = condition_class.sentences
        # new_tokens = []
        for sentence in sentences:
            sentence_index = 0
            for i, token in enumerate(tokens):
                if token.type == sentence[sentence_index]:
                    sentence_index = sentence_index + 1
                    if len(sentence) == sentence_index:
                        # A valid sentense for this condition match => Merge
                        c = condition_class(tokens[i-sentence_index+1:i+1])
                        condition_token = [Token(type=c.getType(), value=c, merged=True)]
                        # new_tokens += [[i-sentence_index+1,len(sentence), condition_token]]
                        # sentence_index = 0
                        # print(tokens[:i-sentence_index+1] + condition_token + tokens[i+1:])
                        return tokens[:i-sentence_index+1] + condition_token + tokens[i+1:],True
                else:
                   sentence_index = 0
        # No any sentense for this condition match => Do nothing
        
        # token_delete = 0
        # for merge in new_tokens :
            # first_token = merge[0]-token_delete
            # last_token = merge[0]+merge[1]- token_delete
            # tokens = tokens[:first_token] + merge[2] + tokens[last_token:]
            # token_delete += merge[1] - 1
        # print("*************")
        # print(condition_class)
        # print(tokens)
        # print("*************")
        return tokens,False