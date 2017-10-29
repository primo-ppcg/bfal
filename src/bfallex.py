from ply import *
import sys
import re

keywords = (
  'WHILE', 'IF', 'ELSE',
  'PLUS', 'MINUS',
  'AND', 'OR', 'NOT',
  'INT', 'STR'
)

tokens = keywords + (
  'EQUALS',
  'LPAREN', 'RPAREN', 'LBRACK', 'RBRACK',
  'INTEGER', 'STRING',
  'ID', 'NEWLINE',
  'BFCODE'
)

keyword_map = {}
for k in keywords:
  keyword_map[k.lower()] = k

bfre = re.compile(r'[-+.,<>\[\]#$!]')

t_ignore = ' \t\r'

def t_COMMENT(t):
  r';.*'
  match = bfre.search(t.value)
  if match:
    sys.stderr.write("Illegal character %r in comment on line %d\n" % (match.group(0), t.lexer.lineno))
    sys.exit(1)
  pass

def t_ID(t):
  r'[A-Za-z][A-Za-z0-9_]*'
  t.type = keyword_map.get(t.value, "ID")
  return t

t_BFCODE = r'[-+.,<>]+'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'

def t_INTEGER(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_STRING(t):
  r'(?P<quote>[\'"])(?:\\(?P=quote)|.)*?(?P=quote)'
  match = bfre.search(t.value)
  if match:
    sys.stderr.write("Illegal character %r in string on line %d\n" % (match.group(0), t.lexer.lineno))
    sys.exit(1)
  t.value = bytearray(eval(t.value))
  return t

def t_NEWLINE(t):
  r'\n'
  t.lexer.lineno += 1
  lex2 = t.lexer.clone()
  toknext = lex2.token()
  if toknext is None or toknext.type in ('NEWLINE', 'LBRACK', 'RBRACK', 'ELSE', 'BFCODE'):
    return None
  return t

def t_error(t):
  sys.stderr.write("Illegal character %r on line %d\n" % (t.value[0], t.lexer.lineno))
  sys.exit(1)


lex.lex(debug=0, optimize=1)

if __name__ == '__main__':
   lex.runmain()
