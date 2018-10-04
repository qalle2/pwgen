# pwgen
Password generator in Python.
Uses the cryptographically strong [``secrets``](http://docs.python.org/3/library/secrets.html) module.
Developed with Python 3 under 64-bit Windows.

## Command line arguments

All arguments are optional.

* `-c` *sets* or `--character-sets`=*sets*
  * Which character sets to use in passwords.
  * *sets* is one or more of the following, in any order:
    * `u`: uppercase letters (see `--uppercase`)
    * `l`: lowercase letters (see `--lowercase`)
    * `d`: digits (see `--digits`)
    * `p`: punctuation (see `--punctuation`)
    * `n`: Unicode characters (see `--unicode`)
  * default: `uldp`
* `-l` *length* or `--length`=*length*
  * How many characters to use in each password.
  * *length* is an integer:
    * minimum: 1
    * default: 16
    * maximum: no limit
* `-a` or `--all-sets`
  * Each password will contain at least one character from each set specified by the `-c` or `--character-sets` option.
* `-r` or `--no-repeat`
  * No password will contain more than two repeated characters. For example, the program may still output `password` but not `passsword` (with three esses).
* `-g` *group_size*, `--group-size`=*group_size*
  * Print passwords in groups of *group_size* characters, separated by spaces.
  * For example, `password` will be printed as `pass&nbsp;word` if *group_size* is 4.
  * Does not affect how the passwords are generated.
  * Good if long passwords must be typed instead of copied and pasted.
  * *group_size* is an integer:
    * minimum: 0 (no grouping)
    * default: 0
    * maximum: no limit
* `-n` *count*, `--number`=*count*
  * How many passwords to generate.
  * *count* is an integer:
    * minimum: 1
    * default: 1
    * maximum: no limit
  * The passwords will be generated independently of each other.
* `--uppercase`=*characters*
  * Define the set of uppercase letters.
  * *characters* is one or more characters.
  * default: `ABCDEFGHIJKLMNOPQRSTUVWXYZ`
* `--lowercase`=*characters*
  * Define the set of lowercase letters.
  * *characters* is one or more characters.
  * default: `abcdefghijklmnopqrstuvwxyz`
* `--digits`=*characters*
  * Define the set of digits.
  * *characters* is one or more characters.
  * default: `0123456789`
* `--punctuation`=*characters*
  * Define the set of punctuation characters.
  * *characters* is one or more characters.
  * default: ```!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~```
* `--unicode`=*codepoints*
  * Define the set of Unicode codepoints.
  * *codepoints* is one or more hexadecimal Unicode codepoints or ranges, separated by commas (`,`).
    * Each range consists of the first codepoint and the last codepoint, separated by a hyphen (`-`).
    * codepoints: `0` to `10ffff`
  * default: `a1-ac,ae-ff`
  * `--settings`
    * Print all settings and exit.
    * for debugging purposes
  * `--alphabet`
    * Print all characters to be used in passwords and exit.
    * for debugging purposes

## Examples

Generate four ASCII passwords of length 10 with at least one uppercase letter, lowercase letter, digit and punctuation character in each one:
```
python pwgen.py --character-sets=uldp --all-sets --length=10 --number=4
8*w/oD\dI%
l3?+Uv1yor
U[h5yWT4^`
x!^'Wr-:2=
```

Generate five passwords of length 20 using *Unicode Miscellaneous Symbols and Pictographs* except `PILE OF POO`:
```
python pwgen.py --character-sets=n --unicode=1f300-1f4a8,1f4aa-1f5ff --length=20 --number=5
🐸🌷🏕🏬🌂🌋🕏📋💖🔁🏐🌆🖮🍲👉🕦📅🐕🖖🍨
📊📰🖊🍓🍹👛👒👖🐇💍🔔💃🏅🕺👯🐅👪🕟🔽🗸
👰🔋🕑👖🖎👶🔹📞🗴🎩👰🕈🗡📕🎀🖓🍃🔐💝💴
🗄📌🕠🖔🍽🐱🎏🍒🐏👆🔧🔼👐🔈🐲🌣🖰💎🕜💪
🎞💯🔱🍋💼🌾🖣🌻🐨🖘👯🍐🐺🏶🖥🕧🖣🕘🖖🕐
```
