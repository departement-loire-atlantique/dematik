# coding: utf8
from jinja2 import Markup

class Condition:

    tokens = []

    sentences = [
            ('CONDITION', 'MESSAGE'),
            ('CONDITION', 'HIDE_PAGE'),
            ('CONDITION', 'HIDE_FIELD')
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
    
    def protect(self, f):
        if 'profil___' in f:
            f = f.replace('profil___prenom', 'form_user_var_first_name')
            f = f.replace('profil___nom', 'form_user_var_last_name')
            f = f.replace('profil___adresse', 'form_user_var_address')
            f = f.replace('profil___commune', 'form_user_var_city')
            f = f.replace('profil___courriel', 'form_user_var_email')
            f = f.replace('profil___telephone_mobile', 'form_user_var_mobile')
            f = f.replace('profil___telephone_fixe', 'form_user_var_phone')
            f = f.replace('profil___civilite', 'form_user_var_title')
            f = f.replace('profil___code_postal', 'form_user_var_zipcode')

        if 'impots___' in f:
            f = f.replace('impots___erreur', 'webservice.api_particulier_impots_svair["err"]')

        if not '_var_' in f and not 'webservice' in f:
            f = 'form_var_' + f
        
        return f

    def build(self):
        return self.condition.build()

    def getExpression(self):
        return Markup(self.build().replace("<", "&lt;"))

    def getMessage(self):
        if hasattr(self, "message"):
            return Markup(self.message)
        else:
            raise Exception("Aucun message pour cette condition")

    def getHiddenFieldname(self):
        if hasattr(self, "hidden_fieldname"):
            return self.hidden_fieldname
        else:
            return ""

    def getPrefillFieldname(self):
        if hasattr(self, "prefill_fieldname"):
            return self.prefill_fieldname
        else:
            return ""

    def getPrefillText(self):
        if hasattr(self, "prefill_value"):
            return self.protect(self.prefill_value)
        elif hasattr(self, "prefill_formula"):
             return self.prefill_formula
        else:
            return ""

    def getDatasourceFieldname(self):
        if hasattr(self, "datasource_fieldname"):
            return self.datasource_fieldname
        else:
            return ""

    def getDatasourceType(self):
        if hasattr(self, "datasource_type"):
            return self.datasource_type
        else:
            return ""

    def getDatasourceValue(self):
        if hasattr(self, "datasource_value"):
            return self.datasource_value
        else:
            return ""

    def __repr__(self):
        return self.build()