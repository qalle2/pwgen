# pwgen
Password generator in Python.
Uses the cryptographically strong [``secrets``](http://docs.python.org/3/library/secrets.html) module.
Developed with Python 3 under 64-bit Windows.

## Command line arguments

Syntax: [*options*] *length*

### *options*

* `-s` *sets* or `--character-sets`=*sets*
  * Which character sets to use in passwords.
  * *sets* is one or more of the following, in any order:
    * `u`: uppercase letters (see `--uppercase`)
    * `l`: lowercase letters (see `--lowercase`)
    * `d`: digits (see `--digits`)
    * `p`: punctuation (see `--punctuation`)
    * `n`: Unicode characters (see `--unicode`)
  * default: `uldp`
* `-a` or `--all-sets`
  * Each password will contain at least one character from each set specified by the `-c` or `--character-sets` option.
* `-g` *length*, `--group-size`=*length*
  * Print passwords in groups of *length* characters, separated by spaces.
  * For example, `password` will be printed as `pass word` if *length* is 4.
  * Does not affect how the passwords are generated.
  * Good if long passwords must be typed instead of copied and pasted.
  * *length* is an integer:
    * minimum: 0 (no grouping)
    * default: 0
    * maximum: no limit
* `-c` *count*, `--count`=*count*
  * How many passwords to generate.
  * *count* is an integer:
    * minimum: 1
    * default: 1
    * maximum: no limit
  * The passwords will be generated independently of each other.
* `-u` *characters*, `--uppercase`=*characters*
  * Define the set of uppercase letters.
  * *characters* is one or more characters.
  * default: `ABCDEFGHIJKLMNOPQRSTUVWXYZ`
* `-l` *characters*, `--lowercase`=*characters*
  * Define the set of lowercase letters.
  * *characters* is one or more characters.
  * default: `abcdefghijklmnopqrstuvwxyz`
* `-d` *characters*, `--digits`=*characters*
  * Define the set of digits.
  * *characters* is one or more characters.
  * default: `0123456789`
* `-p` *characters*, `--punctuation`=*characters*
  * Define the set of punctuation characters.
  * *characters* is one or more characters.
  * default: ```!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~```
* `-n` *characters*, `--unicode`=*codepoints*
  * Define the set of Unicode codepoints.
  * *codepoints* is one or more hexadecimal Unicode codepoints or ranges, separated by commas (`,`).
    * Each range consists of the first codepoint and the last codepoint, separated by a hyphen (`-`).
    * codepoints: `0` to `10ffff`
  * default: `a1-ac,ae-ff`

### *length*
* How many characters to use in each password.
* *length* is an integer:
    * minimum: 1
    * maximum: no limit

## Examples

Generate four alphanumeric ASCII passwords of length 10 with at least one uppercase letter, lowercase letter and digit:
```
python pwgen.py -s uld -a -c 4 10
By6XDrddbW
C6USrm54jj
2frG5TUctI
KQS4gqz3KC
```

Generate five passwords of length 20 using *Unicode Miscellaneous Symbols and Pictographs* except `PILE OF POO`:
```
python pwgen.py --character-sets=n --unicode=1f300-1f4a8,1f4aa-1f5ff --count=5 20
📦🐾🎃🍞💛🍜🕺🐧🏭👹🗴📊🕟🎵🌣🖟🔦💑🍩🍾
🍯💅🖼🍠🔪🖰🔥🕂🗃🌥👧🍤🌏🖡🗽💰🐥🕹🖧📕
🌭🍾💃🍗🔥🖬🗜💮🗧🗿👮🎛📺🕽💮🗻🕱🔍🐝🏌
🔓🐄🐻🎧🔴🗺🕵🌁🔝🌢🍬🐸🏭🖍🗃🖶🕗👂👅🍻
🍿👘🍆🔭🖠🎮🗛🍅🎚🔍🖂👲📎🏮💨💋🏠👦👯🐃
```
