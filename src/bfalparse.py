from ply import *
import bfallex
import sys

class Node:
  def __init__(self, type, *values):
    self.type = type
    self.values = values
    self.count = len(values)

  def __repr__(self):
    return '%s%r'%(self.type, self.values)

  def extend(self, *values):
    self.values += values
    self.count += len(values)

tokens = bfallex.tokens

constants = {
  'tab': "\t", 'newline': "\n", 'space': ' ', 'excl': '!', 'quot': '"', 'num': '#',
  'dollar': '$', 'percnt': '%', 'amp': '&', 'apos': "'", 'lpar': '(', 'rpar': ')',
  'ast': '*', 'plus': '+', 'comma': ',', 'minus': '-', 'period': '.', 'sol': '/',
  'colon': ':', 'semi': ';', 'lt': '<', 'equals': '=', 'gt': '>', 'quest': '?',
  'commat': '@', 'lbrack': '[', 'bsol': '\\', 'rbrack': ']', 'hat': '^', 'lowbar': '_',
  'grave': '`', 'lbrace': '{', 'vert': '|', 'rbrace': '}', 'tilde': '~'
}

precedence = (
  ('left', 'OR'),
  ('left', 'AND'),
  ('right', 'NOT'),
  ('left', 'PLUS', 'MINUS')
)


def p_statement_list1(p):
  '''statement_list : statement_list NEWLINE statement'''
  p[0] = p[1]
  p[0].extend(p[3])


def p_statement_list2(p):
  '''statement_list : statement_list compound_statement
                    | statement_list bfcode_statement'''
  p[0] = p[1]
  p[0].extend(p[2])


def p_statement_list3(p):
  '''statement_list : statement'''
  p[0] = Node('list', p[1])


def p_statement_list4(p):
  '''statement_list : '''
  p[0] = Node('list')


def p_statement1(p):
  '''statement : compound_statement
               | extended_statement
               | if_statement
               | while_statement
               | assign_statement
               | print_statement
               | bfcode_statement'''
  p[0] = p[1]


def p_compound_statement(p):
  '''compound_statement : LBRACK statement_list RBRACK'''
  p[0] =p[2]


def p_extended_statement(p):
  '''extended_statement : compound_statement bfcode'''
  p[0] = Node('list', p[1], p[2])


def p_if_statement1(p):
  '''if_statement : IF LPAREN expr RPAREN statement'''
  p[0] = Node('if', p[3], p[5], None)


def p_if_statement2(p):
  '''if_statement : IF LPAREN expr RPAREN statement ELSE statement'''
  p[0] = Node('if', p[3], p[5], p[7])


def p_while_statement(p):
  '''while_statement : WHILE LPAREN expr RPAREN statement'''
  p[0] = Node('while', p[3], p[5])


def p_assign_statement(p):
  '''assign_statement : variable EQUALS expr_list'''
  p[0] = Node('assign', p[1], p[3])


def p_print_statement(p):
  '''print_statement : expr_list'''
  p[0] = Node('print', p[1])


def p_bfcode_statement(p):
  '''bfcode_statement : bfcode'''
  p[0] = p[1]


def p_variable(p):
  '''variable : ID'''
  if p[1] in constants:
    p.parser.error = 1
  else:
    p[0] = p[1]


def p_expr_list1(p):
  '''expr_list : expr_list expr'''
  p[0] = p[1]
  p[0].extend(p[2])


def p_expr_list2(p):
  '''expr_list : expr'''
  p[0] = Node('list', p[1])


def p_binop_expr(p):
  '''expr : expr PLUS expr
          | expr MINUS expr
          | expr AND expr
          | expr OR expr'''
  p[0] = Node(p[2], p[1], p[3])


def p_unary_expr(p):
  '''expr : NOT expr'''
  p[0] = Node(p[1], p[2])


def p_group_expr(p):
  '''expr : LPAREN expr RPAREN'''
  p[0] = p[2]


def p_cast_expr(p):
  '''expr : STR LPAREN expr RPAREN
          | INT LPAREN expr RPAREN'''
  p[0] = Node(p[1], p[3])


def p_literal_expr(p):
  '''expr : literal'''
  p[0] = p[1]


def p_int_literal(p):
  '''literal : INTEGER'''
  p[0] = Node('integer', p[1])


def p_str_literal(p):
  '''literal : STRING'''
  p[0] = Node('string', p[1])


def p_id_literal(p):
  '''literal : ID'''
  if p[1] in constants:
    p[0] = Node('string', bytearray(constants[p[1]]))
  else:
    p[0] = Node('variable', p[1])


def p_bfcode(p):
  '''bfcode : BFCODE'''
  p[0] = Node('bfcode', p[1])


def p_error(p):
  if p is not None:
    sys.stderr.write('Unexpected token %r (%s) on line %d\n' % (p.value, p.type, p.lineno))
    sys.exit(1)


parser = yacc.yacc(optimize=1)


def parse(data, debug=0):
  return parser.parse(data, debug=debug)


if __name__ == '__main__':
  import sys
  if len(sys.argv) == 2:
    data = open(sys.argv[1]).read()
    prog = parse(data, True)
    print(prog)
