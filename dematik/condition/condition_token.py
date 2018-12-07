import collections

# A sentence token
# - type : Type of the token (semantic meaning)
# - value : sentence words related to this token
# - merged : is this token representing an original token or a merger token
Token = collections.namedtuple('Token', ['type', 'value', 'merged'])