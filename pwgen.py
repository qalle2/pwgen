import getopt
import secrets
import string
import sys

def parse_codepoint(codepoint):
    """Parse a hexadecimal Unicode codepoint."""

    try:
        codepoint = int(codepoint, 16)
        if not 0x0 <= codepoint <= 0x10ffff:
            raise ValueError
    except ValueError:
        exit("Error: invalid Unicode codepoint.")
    return codepoint

def parse_codepoint_range(range_):
    """Parse a hexadecimal Unicode codepoint or a range.
    Return the codepoints in an iterable."""

    items = range_.split("-")
    if len(items) == 1:
        cp = parse_codepoint(items[0])
        return (cp,)
    if len(items) == 2:
        cp1 = parse_codepoint(items[0])
        cp2 = parse_codepoint(items[1])
        if cp1 <= cp2:
            return range(cp1, cp2 + 1)
    exit("Error: invalid Unicode codepoint or range.")

def parse_arguments():
    """Parse command line arguments using getopt."""

    longOptions = (
        "character-sets=",
        "all-sets",
        "no-repeat",
        "group-size=",
        "number=",
        "uppercase=",
        "lowercase=",
        "digits=",
        "punctuation=",
        "unicode=",
        "alphabet",
    )
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "c:arg:n:", longOptions)
    except getopt.GetoptError:
        exit("Error: invalid argument. See the readme file.")

    opts = dict(opts)

    # boolean options
    allSets = "-a" in opts or "--all-sets" in opts
    noRepeat = "-r" in opts or "--no-repeat" in opts
    printAlphabet = "--alphabet" in opts

    # group size
    groupSize = opts.get("--group-size", opts.get("-g", "0"))
    try:
        groupSize = int(groupSize, 10)
        if groupSize < 0:
            raise ValueError
    except ValueError:
        exit("Error: invalid group size.")

    # number of passwords
    number = opts.get("--number", opts.get("-n", "1"))
    try:
        number = int(number, 10)
        if number < 1:
            raise ValueError
    except ValueError:
        exit("Error: invalid number of passwords.")

    # character sets
    charsets = frozenset(opts.get("--character-sets", opts.get("-c", "uldp")))
    if len(charsets - frozenset("uldpn")) > 0:
        exit("Error: unknown character set.")

    # uppercase letters
    uppercase = frozenset(opts.get("--uppercase", string.ascii_uppercase))
    if len(uppercase) == 0:
        exit("Error: no uppercase letters.")

    # lowercase letters
    lowercase = frozenset(opts.get("--lowercase", string.ascii_lowercase))
    if len(lowercase) == 0:
        exit("Error: no lowercase letters.")

    # digits
    digits = frozenset(opts.get("--digits", string.digits))
    if len(digits) == 0:
        exit("Error: no digits.")

    # punctuation
    punctuation = frozenset(opts.get("--punctuation", string.punctuation))
    if len(punctuation) == 0:
        exit("Error: no punctuation characters.")

    # Unicode characters
    ranges_ = opts.get("--unicode", "a1-ac,ae-ff")
    unicode = set()
    for range_ in ranges_.split(","):
        unicode.update(chr(cp) for cp in parse_codepoint_range(range_))

    # password length
    if len(args) != 1:
        exit("Error: invalid number of arguments. See the readme file.")
    length = args[0]
    try:
        length = int(length, 10)
        if length < 1 or (allSets and length < len(charsets)):
            raise ValueError
    except ValueError:
        exit("Error: invalid password length.")

    # return all settings
    return {
        "charsets": charsets,
        "allSets": allSets,
        "noRepeat": noRepeat,
        "groupSize": groupSize,
        "number": number,
        "uppercase": uppercase,
        "lowercase": lowercase,
        "digits": digits,
        "punctuation": punctuation,
        "unicode": unicode,
        "printAlphabet": printAlphabet,
        "length": length,
    }

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
    if settings["printAlphabet"]:
        print("".join(sorted(create_alphabet(settings))))
        exit()

    for i in range(settings["number"]):
        password = generate_password(settings)
        print(format_password(password, settings["groupSize"]))

if __name__ == "__main__":
    main()
