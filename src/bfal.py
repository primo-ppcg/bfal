import sys
from bfalparse import *


nodeResponder = {}
varTable = {}

def register(type, responder):
  nodeResponder[type] = responder

def dispatch(node):
  try:
    return nodeResponder[node.type](node)
  except KeyError:
    sys.stderr.write('Node %r has no registered responder\n' % node.type)
    sys.stderr.write(repr(node))
    sys.exit(1)

def respondsTo(type):
  return lambda responder: register(type, responder)

def toBytearray(values):
  buffer = bytearray()
  for value in values:
    if isinstance(value, int):
      buffer.append(value & 255)
    else:
      buffer += value
  return buffer

def coerceInt(value):
  if isinstance(value, int):
    return value
  return len(value) and value[0]


@respondsTo('string')
def stringResponder(node):
  return node.values[0]

@respondsTo('integer')
def integerResponder(node):
  return node.values[0]

@respondsTo('variable')
def variableResponder(node):
  return varTable.get(node.values[0], 0)

@respondsTo('list')
def listResponder(node):
  return [dispatch(child) for child in node.values]


@respondsTo('or')
def orResponder(node):
  a, b = node.values
  return dispatch(a) or dispatch(b)

@respondsTo('and')
def andResponder(node):
  a, b = node.values
  return dispatch(a) and dispatch(b)

@respondsTo('not')
def notResponder(node):
  return int(not dispatch(node.values[0]))


@respondsTo('plus')
def plusResponder(node):
  a, b = node.values
  return coerceInt(dispatch(a)) + coerceInt(dispatch(b)) & 255

@respondsTo('minus')
def minusResponder(node):
  a, b = node.values
  return coerceInt(dispatch(a)) - coerceInt(dispatch(b)) & 255


@respondsTo('str')
def strResponder(node):
  return bytearray(str(dispatch(node.values[0])))

@respondsTo('int')
def intResponder(node):
  value = dispatch(node.values[0])
  try:
    return int(value)
  except ValueError:
    sys.stderr.write('Invalid literal for int(): %r\n' % value)
    sys.exit(1)


@respondsTo('assign')
def assignResponder(node):
  name, child = node.values
  cvalues = dispatch(child)
  if len(cvalues) == 1:
    varTable[name] = cvalues[0]
  else:
    varTable[name] = toBytearray(cvalues)

@respondsTo('print')
def printResponder(node):
  cvalues = dispatch(node.values[0])
  sys.stdout.write(toBytearray(cvalues))


@respondsTo('if')
def ifResponder(node):
  cond, truebranch, falsebranch = node.values
  if dispatch(cond):
    dispatch(truebranch)
  elif falsebranch is not None:
    dispatch(falsebranch)

@respondsTo('while')
def whileResponder(node):
  cond, block = node.values
  while dispatch(cond):
    dispatch(block)


@respondsTo('bfcode')
def bfcodeResponder(node):
  pass


def main(args):
  if len(args) == 2:
    try:
      data = open(args[1]).read()
      prog = parse(data, False)
      dispatch(prog)
    except IOError:
      sys.stderr.write("Can't open file %r\n"%args[1])
      sys.exit(1)
  else:
    sys.stderr.write('Usage: %s program.bf\n'%args[0])
    sys.exit(1)


if __name__ == '__main__':
  main(sys.argv)