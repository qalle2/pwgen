"""Generates passwords."""

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
        sys.exit("Invalid Unicode codepoint.")
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
    sys.exit("Invalid Unicode codepoint or range.")

def parse_integer_argument(value, minValue, message):
    """Parse a string containing an integer from command line arguments."""

    try:
        value = int(value, 10)
        if value < minValue:
            raise ValueError
    except ValueError:
        sys.exit("Invalid value: " + message)
    return value

def parse_arguments():
    """Parse command line arguments using getopt."""

    shortOptions = "s:g:c:u:l:d:p:n:"
    longOptions = (
        "character-sets=",
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
        sys.exit("Error: invalid command line argument.")
    opts = dict(opts)

    # which character sets to use
    charsets = set(opts.get("--character-sets", opts.get("-s", "uldp")))
    if not charsets or charsets - set("uldpn"):
        sys.exit("Invalid character sets argument.")

    # the alphabet
    alphabet = set()
    if "u" in charsets:
        alphabet.update(opts.get("--uppercase", opts.get("-u", string.ascii_uppercase)))
    if "l" in charsets:
        alphabet.update(opts.get("--lowercase", opts.get("-l", string.ascii_lowercase)))
    if "d" in charsets:
        alphabet.update(opts.get("--digits", opts.get("-d", string.digits)))
    if "p" in charsets:
        alphabet.update(opts.get("--punctuation", opts.get("-p", string.punctuation)))
    if "n" in charsets:
        for range_ in opts.get("--unicode", "a1-ac,ae-ff").split(","):
            alphabet.update(chr(cp) for cp in parse_codepoint_range(range_))
    if not alphabet:
        sys.exit("No characters in sets to use.")

    # group size
    groupSize = opts.get("--group-size", opts.get("-g", "0"))
    groupSize = parse_integer_argument(groupSize, 0, "group size")

    # number of passwords
    count = opts.get("--count", opts.get("-c", "1"))
    count = parse_integer_argument(count, 1, "number of passwords")

    # password length
    if len(args) != 1:
        sys.exit("Error: invalid number of command line arguments.")
    length = parse_integer_argument(args[0], 1, "password length")

    return {
        "alphabet": tuple(alphabet),
        "groupSize": groupSize,
        "count": count,
        "length": length,
    }

def generate_password(settings):
    """Generate one password."""

    return "".join(secrets.choice(settings["alphabet"]) for i in range(settings["length"]))

def group_password(password, groupSize):
    """Split the password into groups."""

    if not groupSize:
        return password
    return " ".join(password[pos:pos+groupSize] for pos in range(0, len(password), groupSize))

def main():
    """The main function."""

    settings = parse_arguments()
    for i in range(settings["count"]):
        print(group_password(generate_password(settings), settings["groupSize"]))

if __name__ == "__main__":
    main()
