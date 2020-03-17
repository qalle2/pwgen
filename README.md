# pwgen
Generate a password using the cryptographically strong secrets module.

## Syntax
```
usage: pwgen.py [-h] [-l LENGTH] [-s SETS] [--uppercase UPPERCASE] [--lowercase LOWERCASE] [--digits DIGITS]
                [--punctuation PUNCTUATION] [--unicode UNICODE]

Generate a password using the cryptographically strong secrets module.

optional arguments:
  -h, --help            show this help message and exit
  -l LENGTH, --length LENGTH
                        The length of the password. (default: 10)
  -s SETS, --sets SETS  Which character sets to use in the password: u=uppercase letters, l=lowercase letters,
                        d=digits, p=punctuation, n=Unicode codepoints. (default: uld)
  --uppercase UPPERCASE
                        The set of uppercase letters. (default: ABCDEFGHIJKLMNOPQRSTUVWXYZ)
  --lowercase LOWERCASE
                        The set of lowercase letters. (default: abcdefghijklmnopqrstuvwxyz)
  --digits DIGITS       The set of digits. (default: 0123456789)
  --punctuation PUNCTUATION
                        The set of punctuation characters. (default: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
  --unicode UNICODE     The hexadecimal Unicode codepoints (0-10ffff). A hyphen ("-") separates the first and last
                        codepoint of a range. A comma (",") separates codepoints and ranges. (default: a1-ac,ae-ff)
```

## Examples
Generate an alphanumeric ASCII password of length 16:
```
C:\>python pwgen.py --length 16 --sets uld
00WVo2T1Wn1DRFma
```

Generate a password of length 32 using *Unicode Miscellaneous Symbols and Pictographs* except `PILE OF POO`:
```
python pwgen.py --length 32 --sets n --unicode 1f300-1f4a8,1f4aa-1f5ff
🍤🖄💯🎑💛👃🗈🖠🗂👠🖇🖣🎒🕥🍽🕭🕻🐨🌥🔻📈🔇💕🍳🎧🕄🖛📽🐂💿🎄🏠
```

## References
* [Python documentation &ndash; the secrets module &ndash; Recipes and best practices](http://docs.python.org/library/secrets.html#recipes-and-best-practices)
