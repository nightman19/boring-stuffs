# Python 3.11
# phoneAndEmail.py - Finds phone numbers and emails in addresses on the clipboard.

import pyperclip, re

phoneRegex = re.compile(r'''(
(\d{3}|\(\d{3}\))?              #area code
(\s|-|\.)?                      #seperator
(\d{3})                         #first 3 digits
(\s|-|\.)                       #seperator
(\d{4})                         #last 4 digits
(\s*(ext|x|ext.)\s*(\d{2,5}))?  #extension
)''', re.VERBOSE)

# create an email regex
emailRegex = re.compile(r'''
[a-zA-Z\d._%+-]+               # username
@                               # @ symbol
[a-zA-Z\d.-]+                  # domain name
(\.[a-zA-Z]{2,4})               #dot-something
''', re.VERBOSE)

# find matches in the clipboard text
text = str(pyperclip.paste())
matches = []
for groups in phoneRegex.findall(text):
    phoneNum = '-'.join([groups[1], groups[3], groups[5]])
    if groups[8] != '':
        phoneNum += ' x' + groups[8]
    matches.append(phoneNum)
for groups in emailRegex.findall(text):
    matches.append(groups[0])

# Copy result to a clipboard
if len(matches) > 0:
    pyperclip.copy('\n'.join(matches))
    print('Copied to clipboard:')
    print('\n'.join(matches))
else:
    print('No problem numbers or email addresses found.')
