import lexer


def main():
  global token
  token = lexer.getToken()
  if lexer.parse_routineDeclaration():
    print 'CORRECT'
  else:
    print "INVALID!"

if __name__ == '__main__':
  main()