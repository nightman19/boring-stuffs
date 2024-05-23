import pyperclip
import re
import textwrap
# passwordRegex = re.compile(r'''(
#     ^(?=.*[A-Z].*[A-Z])                # at least two capital letters
#     (?=.*[!@#$&*])                     # at least one of these special characters
#     (?=.*[0-9].*[0-9])                 # at least two numeric digits
#     (?=.*[a-z].*[a-z].*[a-z])          # at least three lower case letters
#     .{8,}                              # at least 8 total digits
#     $
#     )''', re.VERBOSE)

passwordRegex = re.compile(r'''(
    ^(?=.*[A-Z])                # at least one capital letters
    (?=.*[!@#$&*])              # at least one of these special characters
    (?=.*[0-9])                 # at least one numeric digits
    (?=.*[a-z])                 # at least a lower case letters
    .{8,}                       # at least 8 total characters
    $
    )''', re.VERBOSE)


def checkUserInputPassword():
    ppass = input('Enter a password: ')
    if len(ppass) <= 7:
        print('Please your password short, should be at least 8 character long.')
    else:
        mo = passwordRegex.search(ppass)
        notStronPasswordMessage = '''Password if not strong enough, you\'re encourage to set a stronger password
        A strong password should have at least one uppercase and lowercase letter, 
        one number and at least one of these (!@#$&*) special characters'''
        if not mo:
            print(textwrap.dedent(notStronPasswordMessage))
            return False
        else:
            print('Good work! Your password is strong.')
            return True


checkUserInputPassword()
