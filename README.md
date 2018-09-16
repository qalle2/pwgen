# pwgen
Password generator in Python.
Uses the cryptographically strong [``secrets``](http://docs.python.org/3/library/secrets.html) module.
Developed with Python 3 under 64-bit Windows.

For help, use the `-h` argument: `python pwgen.py -h`

## Example 1

Generate four ASCII passwords of length 10 with at least one uppercase letter, lowercase letter, digit and punctuation character in each one.

### Input

`python pwgen.py --character-sets=uldp --all-sets --length=10 --number=4`

### Output

```
8*w/oD\dI%
l3?+Uv1yor
U[h5yWT4^`
x!^'Wr-:2=
```

## Example 2

Generate five passwords of length 20 using *Unicode Miscellaneous Symbols and Pictographs* except `PILE OF POO`.

### Input

`python pwgen.py --character-sets=n --unicode=1f300-1f4a8,1f4aa-1f5ff --length=20 --number=5`

### Output

```
🐸🌷🏕🏬🌂🌋🕏📋💖🔁🏐🌆🖮🍲👉🕦📅🐕🖖🍨
📊📰🖊🍓🍹👛👒👖🐇💍🔔💃🏅🕺👯🐅👪🕟🔽🗸
👰🔋🕑👖🖎👶🔹📞🗴🎩👰🕈🗡📕🎀🖓🍃🔐💝💴
🗄📌🕠🖔🍽🐱🎏🍒🐏👆🔧🔼👐🔈🐲🌣🖰💎🕜💪
🎞💯🔱🍋💼🌾🖣🌻🐨🖘👯🍐🐺🏶🖥🕧🖣🕘🖖🕐
```
