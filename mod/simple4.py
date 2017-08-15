import string
leet = str.maketrans('abegi','46361')
s = 'The quick brown fox'
print(s)
print(s.translate(leet))
print(string.capwords(s))