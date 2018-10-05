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

def parse_alphabet_arguments(opts):
    """Get the alphabet to use (a frozenset of frozensets)."""

    # which character sets to use
    charsets = set(opts.get("--character-sets", opts.get("-s", "uldp")))
    if not charsets or charsets - set("uldpn"):
        exit("Error: invalid -s/--character-sets argument.")

    alphabet = set()

    if "u" in charsets:
        charset = opts.get("--uppercase", opts.get("-u",
            string.ascii_uppercase
        ))
        alphabet.add(frozenset(charset))
    if "l" in charsets:
        charset = opts.get("--lowercase", opts.get("-l",
            string.ascii_lowercase
        ))
        alphabet.add(frozenset(charset))
    if "d" in charsets:
        charset = opts.get("--digits", opts.get("-d", string.digits))
        alphabet.add(frozenset(charset))
    if "p" in charsets:
        charset = opts.get("--punctuation", opts.get("-p", string.punctuation))
        alphabet.add(frozenset(charset))
    if "n" in charsets:
        charset = set()
        for range_ in opts.get("--unicode", "a1-ac,ae-ff").split(","):
            charset.update(chr(cp) for cp in parse_codepoint_range(range_))
        alphabet.add(frozenset(charset))

    if min(len(charset) for charset in alphabet) == 0:
        exit("Error: a character set is empty.")

    return frozenset(alphabet)

def parse_arguments():
    """Parse command line arguments using getopt."""

    shortOptions = "s:ag:c:u:l:d:p:n:"
    longOptions = (
        "character-sets=",
        "all-sets",
        "group-size=",
        "count=",
        "uppercase=",
        "lowercase=",
        "digits=",
        "punctuation=",
        "unicode=",
    )
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], shortOptions, longOptions)
    except getopt.GetoptError:
        exit("Error: invalid argument. See the readme file.")

    if len(args) != 1:
        exit("Error: invalid number of arguments. See the readme file.")

    opts = dict(opts)

    # alphabet
    alphabet = parse_alphabet_arguments(opts)

    # at least one character from each set?
    allSets = "-a" in opts or "--all-sets" in opts

    # group size
    groupSize = opts.get("--group-size", opts.get("-g", "0"))
    try:
        groupSize = int(groupSize, 10)
        if groupSize < 0:
            raise ValueError
    except ValueError:
        exit("Error: invalid group size.")

    # number of passwords
    count = opts.get("--count", opts.get("-c", "1"))
    try:
        count = int(count, 10)
        if count < 1:
            raise ValueError
    except ValueError:
        exit("Error: invalid number of passwords.")

    # password length
    length = args[0]
    try:
        length = int(length, 10)
        if length < 1 or (allSets and length < len(alphabet)):
            raise ValueError
    except ValueError:
        exit("Error: invalid password length.")

    return {
        "alphabet": alphabet,
        "allSets": allSets,
        "groupSize": groupSize,
        "count": count,
        "length": length,
    }

def generate_password(settings):
    """
    http://docs.python.org/3/library/secrets.html#recipes-and-best-practices
    """

    # create the alphabet
    alphabet = set()
    for charset in settings["alphabet"]:
        alphabet.update(charset)
    alphabet = tuple(alphabet)
    # generate a valid password
    while True:
        password = "".join(
            secrets.choice(alphabet) for i in range(settings["length"])
        )
        if not settings["allSets"] or all(
            charset & frozenset(password) for charset in settings["alphabet"]
        ):
            return password

def format_password(password, groupSize):
    """Return the password with its characters grouped."""

    if groupSize == 0:
        return password
    return " ".join(
        password[pos:pos+groupSize]
        for pos in range(0, len(password), groupSize)
    )

def main():
    settings = parse_arguments()
    for i in range(settings["count"]):
        password = generate_password(settings)
        print(format_password(password, settings["groupSize"]))

if __name__ == "__main__":
    main()
