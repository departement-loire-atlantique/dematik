# coding: utf-8
from yaml import load, YAMLError, FullLoader
from jinja2 import Markup
from htmlentitydefs import codepoint2name
import re

# A field data keep track
class FieldData:

    def __init__(self):
        self.used = set()
        self.charset_encoder = dict((unichr(code), u'&#%s;' % code) for code,name in codepoint2name.iteritems() if code!=38) # exclude "&" 
        self.fields_data = {}

    def htmlescape(self, text):   
        if u"&" in text:
            text = text.replace(u"&", u"&#38;")
        for key, value in self.charset_encoder.items():
            if key in text:
                text = text.replace(key, value)
        return text

    def load(self, filename):
        with open(filename, 'r') as stream:
            yaml_data = load(stream, Loader=FullLoader)
            self.fields_data.update(self.parse(yaml_data))

    def parse(self, fields_data):
        if isinstance(fields_data, list):
            return [self.parse(field_data) for field_data in fields_data]
        if isinstance(fields_data, dict):
            return {self.htmlescape(key):self.parse(field_data) for (key, field_data) in fields_data.items()}
        else:
            if fields_data != None :
                return self.htmlescape(fields_data)
            else:        
                return fields_data

    def __getattr__(self, attribute):
        namespace = ""
        elements = []
        if ':' in attribute:
            namespace, attribute = attribute.split(':')

        if attribute not in self.fields_data:
            raise ValueError("L'attribut " + attribute + " est inconnu")

        field_data = {}
        if isinstance(self.fields_data[attribute], dict):
            for label, items in self.fields_data[attribute].items():
                if isinstance(items, dict):
                    for sous_label, sous_items in items.items():                      
                        nom_sous_label = Markup(sous_label.strip('\n'))
                        if "ligne" in nom_sous_label :
                            lignes =  [Markup(item) for item in sous_items]
                        elif "colonne" in nom_sous_label:
                            colonnes = [Markup(item) for item in sous_items]
                        elif any(element in nom_sous_label for element in ["element","&#233;l&#233;ment"]):
                            elements = [Markup(item) for item in sous_items]
                        else:
                            raise ValueError("L'attribut " + nom_sous_label + " est inconnu")
                    field_data = {
                        "label": Markup(label.strip('\n')),
                        "rows": lignes,
                        "columns": colonnes
                    }
                    if elements != []:
                        field_data["items"] = elements
                        
                else :
                    field_data = {
                        "label": Markup(label.strip('\n')),
                        "items" : [Markup(item) for item in items]
                    }
        else:
            field_data = {
                "label": Markup(self.fields_data[attribute].strip('\n'))
            }

        if namespace:
            field_data["namespace"] = namespace
            
        self.used.add(attribute)
        return field_data

    def unused(self):
        return list(set(self.fields_data) - self.used)
