# pwgen
```
usage: pwgen.py [-h] [-l LENGTH] [-s SETS] [--uppercase UPPERCASE]
                [--lowercase LOWERCASE] [--digits DIGITS]
                [--punctuation PUNCTUATION] [--unicode UNICODE]

Generate a password.

options:
  -h, --help            show this help message and exit
  -l LENGTH, --length LENGTH
                        The length of the password. Default=12.
  -s SETS, --sets SETS  Which character sets to use in the password:
                        u=uppercase letters, l=lowercase letters, d=digits,
                        p=punctuation, n=Unicode. Default=uld.
  --uppercase UPPERCASE
                        The set of uppercase letters. Default: all ASCII
                        uppercase letters.
  --lowercase LOWERCASE
                        The set of lowercase letters. Default: all ASCII
                        lowercase letters.
  --digits DIGITS       The set of digits. Default: all ASCII digits.
  --punctuation PUNCTUATION
                        The set of punctuation characters. Default: all ASCII
                        punctuation characters.
  --unicode UNICODE     A set of additional characters as ranges of
                        hexadecimal Unicode codepoints (0-10ffff). '-'
                        separates the first and last codepoint of a range. ','
                        separates ranges. Default=a1-ac,ae-ff.
```

## Example
```
$ python3 pwgen.py
G84whme85eRf
```
