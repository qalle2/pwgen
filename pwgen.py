"""Generate a password using the cryptographically strong secrets module."""

import argparse
import secrets
import string
import sys

def parse_arguments():
    """Parse command line arguments using argparse."""

    parser = argparse.ArgumentParser(
        description="Generate a password using the cryptographically strong secrets module.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-l", "--length", type=int, default=10, help="The length of the password."
    )
    parser.add_argument(
        "-s", "--sets", default="uld",
        help="Which character sets to use in the password: u=uppercase letters, l=lowercase "
        "letters, d=digits, p=punctuation, n=Unicode codepoints."
    )
    parser.add_argument(
        "--uppercase", default=string.ascii_uppercase, help="The set of uppercase letters."
    )
    parser.add_argument(
        "--lowercase", default=string.ascii_lowercase, help="The set of lowercase letters."
    )
    parser.add_argument(
        "--digits", default=string.digits, help="The set of digits."
    )
    parser.add_argument(
        "--punctuation", default=string.punctuation, help="The set of punctuation characters."
    )
    parser.add_argument(
        "--unicode", default="a1-ac,ae-ff",
        help="The hexadecimal Unicode codepoints (0-10ffff). A hyphen (\"-\") separates the first "
        "and last codepoint of a range. A comma (\",\") separates codepoints and ranges."
    )

    args = parser.parse_args()
    if args.length < 1:
        sys.exit("Invalid password length.")
    if not args.sets:
        sys.exit("Need at least one character set.")
    if set(args.sets) - set("uldpn"):
        sys.exit("No such a character set.")
    return args

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
    """Parse a hexadecimal Unicode codepoint or a range. Return a range()."""

    items = range_.split("-")
    first = parse_codepoint(items[0])
    if len(items) == 1:
        last = first
    elif len(items) == 2:
        last = parse_codepoint(items[1])
        if first > last:
            sys.exit("First codepoint greater than last one in codepoint range.")
    else:
        sys.exit("More than one hyphen in codepoint range.")
    return range(first, last + 1)

def get_alphabet(settings):
    """Get the set of characters to use in passwords."""

    alphabet = set()
    if "u" in settings.sets:
        alphabet.update(settings.uppercase)
    if "l" in settings.sets:
        alphabet.update(settings.lowercase)
    if "d" in settings.sets:
        alphabet.update(settings.digits)
    if "p" in settings.sets:
        alphabet.update(settings.punctuation)
    if "n" in settings.sets:
        for range_ in settings.unicode.split(","):
            alphabet.update(chr(codepoint) for codepoint in parse_codepoint_range(range_))
    if not alphabet:
        sys.exit("No characters in selected sets.")
    return alphabet

def main():
    """The main function."""

    settings = parse_arguments()
    alphabet = get_alphabet(settings)
    print("".join(secrets.choice(list(alphabet)) for i in range(settings.length)))

if __name__ == "__main__":
    main()
