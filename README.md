# pwgen
```
usage: pwgen.py [-h] [-l LENGTH] [-s SETS] [--uppercase UPPERCASE] [--lowercase LOWERCASE]
                [--digits DIGITS] [--punctuation PUNCTUATION] [--unicode UNICODE]

Generate a password using the cryptographically strong secrets module.

optional arguments:
  -h, --help            show this help message and exit
  -l LENGTH, --length LENGTH
                        The length of the password. (default: 10)
  -s SETS, --sets SETS  Which character sets to use in the password: u=uppercase letters,
                        l=lowercase letters, d=digits, p=punctuation, n=Unicode. (default: uld)
  --uppercase UPPERCASE
                        The set of uppercase letters. (default: ABCDEFGHIJKLMNOPQRSTUVWXYZ)
  --lowercase LOWERCASE
                        The set of lowercase letters. (default: abcdefghijklmnopqrstuvwxyz)
  --digits DIGITS       The set of digits. (default: 0123456789)
  --punctuation PUNCTUATION
                        The set of punctuation characters. (default:
                        !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
  --unicode UNICODE     A set of characters as ranges of hexadecimal Unicode codepoints
                        (0-10ffff). A hyphen ('-') separates the first and last codepoint of a
                        range. A comma (',') separates ranges. (default: a1-ac,ae-ff)
```
