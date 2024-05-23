import re


def stripString(s, char=' '):
    stripRegex = re.compile(r'[^'+char+'].*[^'+char+']')
    mo = stripRegex.search(s)
    return mo.group()


sampleText = '    this is    a test      '
text = stripString(sampleText, ' ')

print(text)

sampleText = '             this     is      another       test      '
text = stripString(sampleText)
print(text)

sampleText = 'iiiiiiiiiiithisiiiiiisiiiiiianotheriiiiiiitestiiiiii'
text = stripString(sampleText, 'i')
print(text)
