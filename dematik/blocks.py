from os import listdir,path
from os.path import isfile, join, basename, splitext, dirname, realpath
from re import split

# This class renders blocks (jinja templates)
# 
# n = dematik.Blocks(jinja_env)
# n([block_name, block_param1, block_param2, ...]) renders the block with :
#
#   block_name    : Name of the block
#                   The corresponding block template filename is blocks-xxx/block_name.j2)
#                   If the block_name is followed by a '*' then the block is mandatory
#   block_line_tokens  : The block parameters
#                   Must match block template mandatory parameters
#
# Each block template must specify the mandatory parameters using a comment in 
# the first line like this : {# field_data year -#}
# 
# In this example, block_param1 is attached to field_data template variable
# and block_param2 to year template variable
#
class Blocks:

    def __init__(self, jinja_env, block_dirs):
        self.env = jinja_env

        # Dict : block name (string): block parameters (list)
        self.block_parameters = {}

        # Dict : block name (string): block template path (string)
        self.block_templates = {}

        for block_dir in block_dirs:
            self.load_blocks(block_dir)


    # Load all available blocks from a directory
    def load_blocks(self, path):
        base = dirname(realpath(__file__))
        block_template_names = [t for t in listdir(join(base,path)) if isfile(join(base, path, t))]
        for block_template_name in block_template_names:
            with open(join(base, path, block_template_name)) as f:
                line_tokens = split(r'\s', f.readline().strip())
                if len(line_tokens) < 2 or line_tokens[0] != '{#' or line_tokens[-1] != '-#}':
                    raise Exception("%s : Line 1 - Invalid parameters description. {# var1 var2 ... -#} expected " % block_template_path)
                block_name = splitext(basename(block_template_name))[0]
                self.block_parameters[block_name] = line_tokens[1:-1]
                self.block_templates[block_name] = '/'.join([path, block_template_name])

    def __contains__(self, c):
        return c.replace('*','') in self.block_parameters

    # Block rendering
    #
    # line_tokens (list) : tokenized block definition (one token per word or expression)
    #
    # First token is the block name
    # Following tokens are the block parameters
    def __call__(self, line_tokens):
       
        block_name = line_tokens[0]

        if not block_name in self:
            raise Exception("Le type {} n'existe pas.".format(block_name))

        # Required block
        required = 'False'
        if block_name[-1] == '*':
            required = 'True'
            block_name = block_name[:-1]

        # Block parameters
        block_parameters = self.block_parameters[block_name]
        if len(line_tokens[1:]) != len(block_parameters):
            raise Exception("Le type {} necessite {} argument(s) ({}) et non {}".format(
                block_name, 
                len(block_parameters),
                block_parameters,
                len(line_tokens[1:])))

        template = self.env.get_template(self.block_templates[block_name])
        template_vars = dict(zip(block_parameters,line_tokens[1:]))
        template_vars["required"] = required
        return template.render(template_vars)