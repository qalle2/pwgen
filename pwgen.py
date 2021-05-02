import argparse, secrets, string, sys

def parse_arguments():
    # parse command line arguments using argparse

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
        "letters, d=digits, p=punctuation, n=Unicode."
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
        help="A set of characters as ranges of hexadecimal Unicode codepoints (0-10ffff). A hyphen "
        "('-') separates the first and last codepoint of a range. A comma (',') separates ranges."
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
    # parse a hexadecimal Unicode codepoint
    try:
        codepoint = int(codepoint, 16)
        if not 0 <= codepoint <= 0x10ffff:
            raise ValueError
    except ValueError:
        sys.exit("Invalid codepoint.")
    return codepoint

def parse_codepoint_range(range_):
    # parse a hexadecimal Unicode codepoint or a range, return a range()
    items = range_.split("-")
    if len(items) != 2:
        sys.exit("Invalid codepoint range.")
    (first, last) = (parse_codepoint(i) for i in items)
    if first > last:
        sys.exit("Invalid codepoint range.")
    return range(first, last + 1)

def get_alphabet(args):
    # get the set of characters to use in passwords
    alphabet = set()
    if "u" in args.sets:
        alphabet.update(args.uppercase)
    if "l" in args.sets:
        alphabet.update(args.lowercase)
    if "d" in args.sets:
        alphabet.update(args.digits)
    if "p" in args.sets:
        alphabet.update(args.punctuation)
    if "n" in args.sets:
        for range_ in args.unicode.split(","):
            alphabet.update(chr(codepoint) for codepoint in parse_codepoint_range(range_))
    if not alphabet:
        sys.exit("No characters in selected sets.")
    return alphabet

args = parse_arguments()
alphabet = list(get_alphabet(args))
print("".join(secrets.choice(alphabet) for i in range(args.length)))
