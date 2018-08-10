import getopt
import secrets
import string
import sys

DEFAULT_UNICODE = "a1-ac,ae-ff"

HELP_TEXT = """\
Password generator by Kalle (http://qalle.net)

Arguments (all optional):
    -h, -?, --help
        Print help and exit.
    -c X, --character-sets=X
        Character sets to use in passwords.
        X consists of one or more of the following, in any order:
            u   uppercase letters (see the --uppercase option)
            l   lowercase letters (see the --lowercase option)
            d   digits (see the --digits option)
            p   punctuation (see the --punctuation option)
            n   Unicode characters (see the --unicode option)
        Default: uldp
    -l X, --length=X
        Length of passwords.
        X is a positive integer. Default: 16
    -a, --all-sets
        Each password will contain at least one character from each set
        specified by the -c/--character-sets option.
    -r, --no-repeat
        No password will contain more than two repeated characters.
        For example, "password" will still be valid but "passsword" (with
        three esses) will not.
    -g X, --group-size=X
        Print passwords in groups of X characters, separated by spaces.
        Does not affect how passwords are generated. Good if the passwords
        must be typed instead of copied and pasted.
        X is a nonnegative integer. 0 means no grouping. Default: 0
    -n X, --number=X
        Number of passwords to generate.
        The passwords are generated independently of each other.
        X is a positive integer. Default: 1
    --uppercase=X
        Define the set of uppercase letters. (You may not want I or O, for
        example.)
        X is one or more characters.
        Default: {defaultUppercase:s}
    --lowercase=X
        Define the set of lowercase letters. (You may not want l or o, for
        example.)
        X is one or more characters.
        Default: {defaultLowercase:s}
    --digits=X
        Define the set of digits. (You may not want 0 or 1, for example.)
        X is one or more characters.
        Default: {defaultDigits:s}
    --punctuation=X
        Define the set of punctuation characters. (You may not want those
        missing from your mobile device's keyboard, for example.)
        X is one or more characters.
        Default: {defaultPunctuation:s}
    --unicode=X
        Define the set of Unicode characters.
        X is one or more hexadecimal Unicode codepoints or ranges,
        separated by commas. Each range consists of the first codepoint
        and the last codepoint, separated by a hyphen. Codepoints are 0
        to 10ffff.
        Default: {defaultUnicode:s}
    --settings
        Print all settings and exit. (For debugging purposes.)
    --alphabet
        Print all characters to be used in passwords and exit. (For
        debugging purposes.)\
""".format(
    defaultUppercase = string.ascii_uppercase,
    defaultLowercase = string.ascii_lowercase,
    defaultDigits = string.digits,
    defaultPunctuation = string.punctuation,
    defaultUnicode = DEFAULT_UNICODE,
)

def parse_argument(opts, argument1, argument2):
    """Parse getopt argument.
        opts: from getopt
        argument1: name (e.g. "--number")
        argument2: alternative name (e.g. "-n") or None
    If argument is not given, return None.
    If argument is given and empty, exit.
    If argument is given and not empty, return it."""
    value = opts.get(argument1)
    if value is None and argument2 is not None:
        value = opts.get(argument2)
    if value is not None and len(value) == 0:
        exit("Error: invalid value for the {:s}{:s} option.".format(
            argument1, ("" if argument2 is None else "/" + argument2)
        ))
    return value

def parse_string_argument(opts, argument1, argument2, default):
    """Parse getopt string argument.
        opts: from getopt
        argument1: name (e.g. "--text")
        argument2: alternative name (e.g. "-t") or None
        default: str
    If argument is not given, return default as frozenset.
    If argument is given and empty, exit.
    If argument is given and not empty, return it as frozenset."""
    value = parse_argument(opts, argument1, argument2)
    return frozenset(default if value is None else value)

def parse_integer_argument(opts, argument1, argument2, minimum, default):
    """Parse getopt argument.
        opts: from getopt
        argument1: name (e.g. "--number")
        argument2: alternative name (e.g. "-n") or None
        minimum: int
        default: int
    If argument is not given, return default.
    If argument is given and invalid, exit.
    If argument is given and valid, return it."""
    value = parse_argument(opts, argument1, argument2)
    if value is None:
        return default
    try:
        value = int(value, 10)
    except ValueError:
        exit("Error: value is not an integer.")
    if value < minimum:
        exit("Error: integer value is too small.")
    return value

def parse_codepoint(codepoint):
    """Parse a hexadecimal codepoint (str)."""
    try:
        codepoint = int(codepoint, 16)
        if not 0x0 <= codepoint <= 0x10ffff:
            exit("Error: Unicode codepoint out of range.")
    except ValueError:
        exit("Error: Unicode codepoint is not a hexadecimal integer.")
    return codepoint

def parse_codepoint_range(range_):
    """Parse a hexadecimal codepoint or a range (str).
    return: codepoints in an iterable"""
    if len(range_) == 0:
        exit("Error: empty Unicode codepoint/range.")
    codepoints = tuple(parse_codepoint(part) for part in range_.split("-"))
    if len(codepoints) == 1:
        return (codepoints[0],)
    if len(codepoints) == 2 and codepoints[0] <= codepoints[1]:
        return range(codepoints[0], codepoints[1] + 1)
    exit("Error: invalid Unicode codepoint/range.")

def parse_unicode_argument(opts):
    """Parse --unicode argument.
    return: characters in a frozenset"""
    ranges = opts.get("--unicode", DEFAULT_UNICODE)
    if len(ranges) == 0:
        exit("Error: empty list of Unicode codepoints/ranges.")
    chars = set()
    for range_ in ranges.split(","):
        chars.update(chr(cp) for cp in parse_codepoint_range(range_))
    return frozenset(chars)

def parse_arguments():
    longOptions = [
        "help",
        "character-sets=",
        "length=",
        "all-sets",
        "no-repeat",
        "group-size=",
        "number=",
        "uppercase=",
        "lowercase=",
        "digits=",
        "punctuation=",
        "unicode=",
        "settings",
        "alphabet",
    ]
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "h?c:l:arg:n:", longOptions)
    except getopt.GetoptError:
        exit("Error: unrecognized argument. Try -h for help.")
    if len(args) > 0:
        exit("Error: unrecognized argument. Try -h for help.")

    opts = dict(opts)

    # parse boolean arguments
    printHelp = "-h" in opts or "-?" in opts or "--help" in opts
    allSets = "-a" in opts or "--all-sets" in opts
    noRepeat = "-r" in opts or "--no-repeat" in opts
    printSettings = "--settings" in opts
    printAlphabet = "--alphabet" in opts

    # parse integer arguments
    length = parse_integer_argument(opts, "--length", "-l", 1, 16)
    groupSize = parse_integer_argument(opts, "--group-size", "-g", 0, 0)
    number = parse_integer_argument(opts, "--number", "-n", 1, 1)

    # parse string arguments
    charsets = parse_string_argument(opts, "--character-sets", "-c", "uldp")
    uppercase = parse_string_argument(opts, "--uppercase", None, string.ascii_uppercase)
    lowercase = parse_string_argument(opts, "--lowercase", None, string.ascii_lowercase)
    digits = parse_string_argument(opts, "--digits", None, string.digits)
    punctuation = parse_string_argument(opts, "--punctuation", None, string.punctuation)

    # parse Unicode argument
    unicode = parse_unicode_argument(opts)

    # misc validation
    if allSets and length < len(charsets):
        exit("Error: passwords must be longer to satisfy requirements.")
    if len(charsets - frozenset("uldpn")) > 0:
        exit("Error: unknown character set.")

    # return all settings
    return {
        "printHelp": printHelp,
        "charsets": charsets,
        "length": length,
        "allSets": allSets,
        "noRepeat": noRepeat,
        "groupSize": groupSize,
        "number": number,
        "uppercase": uppercase,
        "lowercase": lowercase,
        "digits": digits,
        "punctuation": punctuation,
        "unicode": unicode,
        "printSettings": printSettings,
        "printAlphabet": printAlphabet,
    }

def print_settings(settings):
    """Print all settings."""
    for key in sorted(settings):
        try:
            value = sorted(settings[key])
        except TypeError:
            value = settings[key]
        print("{:s}: {!s}".format(key, value))

def get_selected_charsets(settings):
    """Yield contents of each selected character set."""
    for (charset, contents) in (
        ("u", "uppercase"),
        ("l", "lowercase"),
        ("d", "digits"),
        ("p", "punctuation"),
        ("n", "unicode"),
    ):
        if charset in settings["charsets"]:
            yield settings[contents]

def create_alphabet(settings):
    """Get a list of all characters in selected sets."""
    alphabet = set()
    for charset in get_selected_charsets(settings):
        alphabet.update(charset)
    return list(alphabet)

def validate_password(password, settings):
    """Return True if password is valid or False if it is not."""

    if settings["allSets"]:
        # reject if there is not at least one character from each set
        uniqueChars = frozenset(password)
        if any(
            charset.isdisjoint(uniqueChars)
            for charset in get_selected_charsets(settings)
        ):
            return False

    if settings["noRepeat"]:
        # reject if there are three repeated letters
        for pos in range(0, len(password) - 2):
            if len(set(password[pos:pos+3])) == 1:
                return False

    # accept
    return True

def generate_password(settings):
    """http://docs.python.org/3/library/secrets.html#recipes-and-best-practices
    """

    alphabet = create_alphabet(settings)

    # generate passwords until one passes the tests
    while True:
        password = "".join(
            secrets.choice(alphabet) for i in range(settings["length"])
        )
        if validate_password(password, settings):
            return password

def format_password(password, groupSize):
    """Return password with its characters grouped."""

    if groupSize == 0:
        return password

    return " ".join(
        password[pos:pos+groupSize]
        for pos in range(0, len(password), groupSize)
    )

def main():
    settings = parse_arguments()
    if settings["printHelp"]:
        print(HELP_TEXT)
        exit()
    if settings["printSettings"]:
        print_settings(settings)
        exit()
    if settings["printAlphabet"]:
        print("".join(sorted(create_alphabet(settings))))
        exit()

    for i in range(settings["number"]):
        password = generate_password(settings)
        print(format_password(password, settings["groupSize"]))

if __name__ == "__main__":
    main()
