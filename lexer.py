import re

token = ''
Tokens = []

def getToken():
  global Tokens
  global token
  if not Tokens:
    Tokens = raw_input()
    Tokens = Tokens.split()
  token = Tokens.pop(0)
  return token


def findInt():
  global token
  match = re.match('[+-]?\d+', token)
  return match


def findDec():
  global token
  match = re.match('[+-]?\d+\.\d+', token)
  return match


def findStr():
  global token
  match = re.match('"\S+"', token)
  return match


def findKey():
  global token
  match = False
  if token == '<=':
    match = True
  elif token == '+':
    match = True
  elif token == '-':
    match = True
  elif token == '*':
    match = True
  elif token == '/':
    match = True
  elif token == 'or':
    match = True
  elif token == 'and':
    match = True
  elif token == '~':
    match = True
  elif token == '(':
    match = True
  elif token == ')':
    match = True
  elif token == 'lt':
    match = True
  elif token == 'gt':
    match = True
  elif token == 'eq':
    match = True
  elif token == '<':
    match = True
  elif token == '>':
    match = True
  elif token == '!':
    match = True
  elif token == 'print':
    match = True
  elif token == 'inc':
    match = True
  elif token == 'ret':
    match = True
  elif token == 'if':
    match = True
  elif token == 'fi':
    match = True
  elif token == 'else':
    match = True
  elif token == 'while':
    match = True
  elif token == 'elihw':
    match = True
  elif token == 'defprog':
    match = True
  elif token == 'blip':
    match = True
  elif token == 'blorp':
    match = True
  return match


def findIdent():
  global token
  match = re.match(r'[a-zA-z]\w*', token) and not findKey()
  return match


def parse_relation():
  global token
  stillWorking = False
  if token == 'lt':
    stillWorking = True
  elif token == 'gt':
    stillWorking = True
  elif token == 'eq':
    stillWorking = True
  return stillWorking


def parse_addOperator():
  global token
  stillWorking = False
  if token == '+':
    stillWorking = True
  elif token == '-':
    stillWorking = True
  elif token == 'or':
    stillWorking = True
  return stillWorking


def parse_mullOperator():
  global token
  stillWorking = False
  if token == '*':
    stillWorking = True
  elif token == '/':
    stillWorking = True
  elif token == 'and':
    stillWorking = True
  return stillWorking


def parse_expression():
  global token
  stillWorks = False
  if parse_simpleExpression():
    stillWorks = True
    if parse_relation():
      token = getToken()
      stillWorks = parse_simpleExpression()
  return stillWorks


def parse_simpleExpression():
  global token
  stillWorks = False
  if parse_term():
    stillWorks = True
    while parse_addOperator():
      token = getToken()
      stillWorks = parse_term()
  return stillWorks


def parse_term():
  global token
  stillWorks = False
  if parse_factor():
    stillWorks = True
    token = getToken()
    while parse_mullOperator():
      token = getToken()
      if not parse_factor():
        stillWorks = False
  return stillWorks


def parse_factor():
  global token
  stillWorks = False
  if findInt():
    stillWorks = True
  elif findDec():
    stillWorks = True
  elif findStr():
    stillWorks = True
  elif findIdent():
    stillWorks = True
  elif token == '(':
    token = getToken()
    if parse_expression():
      if token == ')':
        stillWorks = True
  elif token== '~':
    token = getToken()
    if parse_factor():#return here last
      stillWorks = True
  return stillWorks


def parse_assignment():
  global token
  stillWorks = False
  if findIdent():
    token = getToken()
    if token == '<=':
      token = getToken()
      if parse_expression():
        if token == '!':
          stillWorks = True
  return stillWorks


def parse_incStatement():
  global token
  stillWorks = False
  if token == 'inc':
    token = getToken()
    if findIdent():
      token = getToken()
      if token == '!':
        stillWorks = True
  return stillWorks


def parse_ifStatement():
  global token
  stillWorks = False
  if token == 'if':
    token = getToken()
    if token == '<':
      token = getToken()
      if parse_expression():
        if token == '>':
          token = getToken()
          if parse_statementSequence():
            if token == 'else':
              token = getToken()
              if parse_statementSequence():
                if token == 'fi':
                  stillWorks = True
            elif token == 'fi':
              stillWorks = True
  return stillWorks


def parse_loopStatement():
  global token
  stillWorks = False
  if token == 'while':
    token = getToken()
    if token == '<':
      token = getToken()
      if parse_expression():
        if token == '>':
          token = getToken()
          if parse_statementSequence():
            if token == 'elihw':
              stillWorks = True
  return stillWorks


def parse_printStatement():
  global token
  stillWorks = False
  if token == 'print':
    token = getToken()
    if findIdent():
      token = getToken()
      if token == '!':
        stillWorks = True
  return stillWorks


def parse_statement():
  global token
  stillWorks = True
  if findIdent():
    stillWorks = parse_assignment()
  elif token == 'inc':
    stillWorks = parse_incStatement()
  elif token == 'if':
    stillWorks = parse_ifStatement()
  elif token == 'while':
    stillWorks = parse_loopStatement() #return from loop
  elif token == 'print':
    stillWorks = parse_printStatement()
  return stillWorks


def parse_statementSequence():
  global token
  stillWorks = False
  if parse_statement():
    stillWorks = True
    token = getToken()
  while findIdent() or token == 'inc' or token == 'if' or token == 'while' or token == 'print':
    stillWorks = parse_statement()
    token = getToken()
  return stillWorks


def parse_paramSequence():
  global token
  stillWorks = False
  if findIdent():
    stillWorks = True
    token = getToken()
    while token == ',':
      token = getToken()
      stillWorks = findIdent()
      token = getToken()
  return stillWorks


def parse_routineDeclaration():
  global token
  works = False
  param = True
  SS = True
  Express = True
  while True:
    if token == 'defprog':
      token = getToken()
      if findIdent():
        token = getToken()
        if token == '<':
          token = getToken()
          if not token == '>':
            param = parse_paramSequence()
          if not param:
            break
          if token == '>':
            token = getToken()
            if token == 'blip':
              token = getToken()
              if findIdent() or token == 'inc' or token == 'if' or token == 'while' or token == 'print':
                SS = parse_statementSequence()
              if not SS:
                break
              if token =='ret':
                token = getToken()
                Express = parse_expression()
              if not Express:
                break
              if token == 'blorp':
                works = True
    break
  return works and param and SS and Express

