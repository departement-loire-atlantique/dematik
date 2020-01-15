# coding: utf8
from __future__ import print_function
from jinja2 import Environment, PackageLoader, PrefixLoader, Markup, select_autoescape, StrictUndefined
from collections import Counter
from datetime import datetime
from .field_data import FieldData
import condition 
from blocks import Blocks
from markdown import markdown
from os.path import isfile, dirname
from lxml import etree
import traceback
import jinja2.exceptions
import json
import re
import os

# This class allows to build process and forms form its definition
class Dematik:

    def __init__(self, backend, debug=False):
        # Debug mode means printing stack trace on errors
        self.debug = debug
        
        self.env = Environment(
            loader=PrefixLoader({
                'blocks-'+backend:   PackageLoader('dematik', 'blocks-'+backend),
                'macros-'+backend:   PackageLoader('dematik', 'macros-'+backend)
            }),
            autoescape=select_autoescape(['j2']),
            undefined=StrictUndefined
        )

        self.env.globals = {
            "now": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "get_text" : self.get_text,
            "get_md_text" : self.get_md_text,
            "get_items" : self.get_items,
            "get_varname" : self.get_varname,
            "get_id" : self.get_id,
            "is_in_listing" : self.is_in_listing,
            "is_in_filters" : self.is_in_filters,
        }

        self.fields_data = FieldData()
        self.blocks = Blocks(self.env, ['blocks-'+backend])
        self.reset()

    # Returns text or raise a ValueError
    def get_text(self, field_data):
        if len(field_data) > 1 and field_data[0] == '"' and field_data[-1] == '"':
            return Markup(self.fields_data.htmlescape(field_data[1:-1].decode('utf-8')))
        else:
            return getattr(self.fields_data, field_data)["label"]

    # Returns html from a markdown compatible text or raise a ValueError
    def get_md_text(self, field_data):
        return markdown(getattr(self.fields_data, field_data)["label"])
    
    # Returns a list of items or raise a ValueError
    def get_items(self, field_data):
        return getattr(self.fields_data, field_data)["items"]

     # Returns a varname or raise a ValueError
    def get_varname(self, field_data):
        return field_data.replace(':', '___')

     # Generate ID for form fields using a cache process
    def get_id(self, field_data=None):
        id = self.id

        # ID in cache for this field ?
        if field_data and field_data in self.ids_cache:
            # yes
            id = self.ids_cache[field_data]
        else:
            # no : generate a new ID and add it to the cache
            self.id += 1
            id = self.id
            if field_data:
                self.ids_cache[field_data] = id

        # Check that field_data is unique
        if field_data and field_data in self.used_field_data:
            raise Exception("Le nom %s a deja ete utilise. Merci d'utiliser d'ajouter un contexte ou creer un nouveau code" % field_data)
        elif field_data:
            self.used_field_data += [field_data]
       
        return id

    # Returns if a field should appear in listing
    def is_in_listing(self, field_data):
        return str(field_data in self.in_listing)

    # Returns if a field should appear in filters
    def is_in_filters(self, field_data):
        return str(field_data in self.in_filters)

    # Load field data from a file
    def load_field_data(self, path):
        self.fields_data.load(path)

    # Reset context
    # Should be done before each definition file process 
    def reset(self):
        # form name
        self.form = None

        # form metadata
        self.env.globals["formulaire"] = {
                "workflow":"Par d&#233;faut",
                "category_id": "",
                "category_name": "",
                "user_roles_id": "",
                "user_roles_name": "",
                "backoffice_submission_roles_id": "",
                "backoffice_submission_roles_name": "",
                "roles_id": "",
                "roles_key": "",
                "roles_name": "",
                }
        self.env.globals["workflow_options"] = {}

        # form fields (XML)
        self.form_fields_as_xml = ""

        # form prefill
        self.env.globals["prefill_formulas"] = {}

        # datasources
        self.env.globals["datasources"] = {}
        
        # current page (buffer)
        self.current_page = None
        self.current_page_conditions = []
        self.current_page_post_conditions = []
        self.current_page_field_conditions = []
        self.current_page_fields = []

        # Used field code table (to prevent duplicate ID)
        self.used_field_data = []

        # form field id counter
        self.id = 1

        # ID cache dict : field data (string) : id (string)
        self.ids_cache = {}

        # list of fields that should appear in the admin listing
        self.in_listing = []

        # list of fields that should appear in the admin filters
        self.in_filters = []

    # Parse "formulaire" metadata
    def parseFormMetadata(self, tokens):
        metas = [
                "description", "identifiant", "url", "workflow",
                "category_id", "category_name",
                "user_roles_id", "user_roles_name",
                "backoffice_submission_roles_id", "backoffice_submission_roles_name",
                "roles_id", "roles_key", "roles_name"
                ]

        for meta in metas:
            if tokens[0] == meta and len(tokens) == 2:
                self.env.globals["formulaire"][meta] = self.get_text(tokens[1])
                return True

        if tokens[0] == "listing" and len(tokens) == 2:
            self.in_listing.append(tokens[1])
            return True

        if tokens[0] == "filter" and len(tokens) == 2:
            self.in_filters.append(tokens[1])
            return True

        worflow_option = re.search(r'Le paramètre (?P<key>.*) du workflow vaut (?P<val>.*)', ' '.join(tokens))
        if worflow_option:
            wo = self.env.globals["workflow_options"]
            wo[self.get_text(worflow_option.group("key"))] = self.get_text(worflow_option.group("val"))
            return True

        return False

    def merge_and_invert_conditions(self, conditions):
        condition = ""
        if conditions:
            condition = 'not %s' % conditions[0].build()
            conditions = conditions[1:]
            for cond in conditions:
                condition = '%s and not %s' % (condition, cond.build())
        
        return Markup(condition.replace("<", "&lt;"))

    def render_current_form_page(self):
        if self.current_page:
            if not self.current_page_post_conditions:
                self.current_page_post_conditions += []

            # Merge hide page conditions into a unique condition
            self.env.globals["post_conditions"] = self.current_page_post_conditions
            self.env.globals["condition"] = self.merge_and_invert_conditions(self.current_page_conditions)
            self.form_fields_as_xml += self.blocks(self.current_page)

            for current_page_field in self.current_page_fields:
                current_page_fielddata = current_page_field["t"]
                conds = [c for c in self.current_page_field_conditions if c.getHiddenFieldname().replace('___', ':') in current_page_fielddata]
                self.env.globals["condition"] = self.merge_and_invert_conditions(conds)
                self.env.globals["hint"] = current_page_field["hint"]
                self.env.globals["extra_css_class"] = ""
                self.form_fields_as_xml += self.blocks(current_page_fielddata)

    # Parse form fields
    def parseFieldBlock(self, tokens):
        if tokens[0] in self.blocks:
            if "page" in tokens[0]:
                # Generate previous page
                self.render_current_form_page()

                # Create a new page
                self.current_page = tokens
                self.current_page_conditions = []
                self.current_page_post_conditions = []
                self.current_page_fields = []
                self.current_page_field_conditions = []
              
            elif "formulaire" in tokens[0]:
                # Form is rendered at the end of the process, safe this line
                self.form = tokens

            else:
                self.current_page_fields += [{"t":tokens, "hint":""}]

            return True

        if tokens[0] == 'si' or tokens[0] == 'préremplir' or tokens[0] == 'lier':
            c = condition.ConditionParser()
            cond = c.parse(' '.join(tokens))

            if cond.type == 'CONDITION_LEAVE_PAGE':
                self.current_page_post_conditions += [cond]
            elif cond.type == 'CONDITION_HIDE_PAGE':
                self.current_page_conditions += [cond]
            elif cond.type == 'CONDITION_HIDE_FIELD' :
                self.current_page_field_conditions += [cond]
            elif cond.type == 'PREFILL' :
                self.env.globals["prefill_formulas"][cond.getPrefillFieldname()] = cond.getPrefillText() 
            elif cond.type == 'DATASOURCE' :
                datasource = {'type' : cond.getDatasourceType()}
                if 'json' != cond.getDatasourceType() and 'jsonp' != cond.getDatasourceType() and 'formula' != cond.getDatasourceType():
                    datasource['type'] = self.get_text(cond.getDatasourceType())
                if cond.getDatasourceValue():
                    datasource['value'] = self.get_text(cond.getDatasourceValue()) if 'formula' != cond.getDatasourceType() else Markup(cond.getDatasourceValue()[1:-1])
                self.env.globals["datasources"][cond.getDatasourceFieldname()] = datasource
            return True

        if ' '.join(tokens[0:4]) == 'aide à la saisie':
            self.current_page_fields[-1]["hint"] = tokens[4]
            return True
        
        # Line could not be parsed, first token is unknown
        return False

    # Convert a process definition to a form file
    def render_form(self, path):
        context = ""
        try:
            with open(path, 'r') as f:
                for i, line in enumerate(f):
                    tokens = re.findall(r'[^"\s]\S*|".+?"', line.strip())

                    # Ignore empty line or comment lines
                    if len(tokens) > 0 and tokens[0] and tokens[0][0] != '#':
                        context = path + ' line ' + str(i+1)
                        if not (self.parseFormMetadata(tokens)
                            or self.parseFieldBlock(tokens)):
                            print("{} - WARN - Ligne ignoree - Bloc {} n'est pas implemente, veuillez l'implementer".format(
                                    context,
                                    tokens[0]))
        
        except Exception as e:
            if self.debug:
                traceback.print_exc()
            print(context + " - ERROR - " + str(e))
            return None
       
        # Generate form
        if self.form:
            self.render_current_form_page()
            return self.blocks(self.form + [Markup(self.form_fields_as_xml)])
            
        print("ERROR - Il manque le nom du formulaire")
        return None
                
    # Process definition
    def generate(self, path, force=False):

        self.reset()

        id_before_parse = 0
        base_path = path.replace('definitions', 'generated') \
                    .replace('.def', '')
        wcs_filename = base_path + '.wcs'

        # Load ID cache
        if isfile(wcs_filename):
            try:
                tree = etree.parse(wcs_filename)
                for id_elem in tree.xpath("//id"):
                    if 'remote' in id_elem.attrib:
                        self.ids_cache[id_elem.attrib['remote']] = int(id_elem.text)
                    else:
                        print("%s - FATAL - Element has no remote ID" % (path))
                        return
                if self.ids_cache.values():
                        self.id = max(self.ids_cache.values())
                        id_before_parse = self.id

                # Skip generation if .wcs file is newer than .def file
                if not force and os.stat(wcs_filename).st_mtime > os.stat(path).st_mtime:
                    print("%s - INFO - Skipped - Nothing new" % (path))
                    return

            except:
                self.ids_cache = {}
        
        if not id_before_parse:
            print("%s - WARN - Generation des ID sans cache" % path)

        # Render form
        form = self.render_form(path)
        if not form:
            print("%s - FATAL - Abandon de generation" % path)
            return
        
        # Create export directory if needed
        if not os.path.exists(dirname(base_path)):
            os.makedirs(dirname(base_path))

        # Save generated form
        with open(wcs_filename, 'w+') as f:
            f.write(form)

        # Check that every ID element has a remote ID
        tree = etree.parse(wcs_filename)
        for i in tree.xpath("//id"):
            if not 'remote' in i.attrib:
                print("%s - FATAL - Element has no remote ID" % (path))
                return

        # Some stats
        print('{} - OK - Nombre exigences : {} ({})'.format(path, len(self.used_field_data), self.id - id_before_parse - 1))

    # Print field data that has not been used yet 
    def show_unused_labels(self):
        print('Unused YAML labels')
        for label in self.fields_data.unused():
            print(" - " + label)
