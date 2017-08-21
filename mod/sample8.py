import re
text = 'Does this text match the pattern?'
print('Text: %r\n' % text)

for regex in [ 'this','that']:
    print('Seeking "%s" ->' % regex.pattern)
    if(regex.search(text)):
        print('match!')
    else:
        print('no match!')