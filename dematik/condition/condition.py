# coding: utf8
from jinja2 import Markup

class Condition:

    tokens = []

    sentences = [
            ('CONDITION', 'MESSAGE'),
            ('CONDITION', 'HIDE_PAGE'),
            ('CONDITION', 'HIDE_FIELD'),
    ]

    def __init__(self, tokens):
        
        self.condition=tokens[0].value

        if tokens[1].type == 'MESSAGE':
            self.type = "CONDITION_LEAVE_PAGE"
            self.message=tokens[1].value.message
        elif tokens[1].type == 'HIDE_PAGE':
            self.type = "CONDITION_HIDE_PAGE"
        else:
            self.type = "CONDITION_HIDE_FIELD"
            self.hidden_fieldname = tokens[1].value.hidden_fieldname

    def getType(self):
        return self.type
    
    def protect(self, f, language):
        if '_var_' in f:
            return f
        else:
            return 'form_var_' + f


    def protect_as_list(self, field, language):
        if language == 'python':
            f = self.protect(field, language)
            return f + ' if isinstance(' + f + ', list) else ([' + f + '] if ' + f + ' else [])'
        elif language == 'django':
            return self.protect(field, language) 
        else:
            raise Exception('not implemented')

    def build(self, language):
        return self.condition.build(language)

    def getPythonExpression(self):
        return Markup(self.build('python'))

    def getMessage(self):
        if hasattr(self, "message"):
            return self.message
        else:
            raise Exception("Aucun message pour cette condition")

    def getHiddenFieldname(self):
        if hasattr(self, "hidden_fieldname"):
            return self.hidden_fieldname
        else:
            raise Exception("Aucun nom de champ pour cette condition")

    def __repr__(self):
        return self.build('python')