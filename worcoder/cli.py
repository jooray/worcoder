#!/usr/bin/env python3

import argparse
from worcoder.encoding import str_to_mnemonic, mnemonic_to_str

def main():
    parser = argparse.ArgumentParser(
        description="Simple CLI for worcoder: convert strings <-> mnemonic."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--encode",
        action="store_true",
        help="Encode the following arguments into a mnemonic."
    )
    group.add_argument(
        "--decode",
        action="store_true",
        help="Decode the following arguments from a mnemonic to a string."
    )
    parser.add_argument(
        "--ascii-only",
        action="store_true",
        help="Use ASCII-only compression for encoding/decoding."
    )
    parser.add_argument(
        "data",
        nargs="*",
        help="The data or mnemonic words. All will be joined with spaces."
    )
    args = parser.parse_args()

    # Join all leftover arguments into a single string (separated by spaces).
    joined_input = " ".join(args.data)

    if args.encode:
        # Encode the joined input as a mnemonic string.
        output = str_to_mnemonic(joined_input, ascii_only=args.ascii_only)
    else:
        # Decode the joined input from mnemonic -> original string.
        output = mnemonic_to_str(joined_input, ascii_only=args.ascii_only)

    # Print result without adding an extra newline.
    print(output, end="")

if __name__ == "__main__":
    main()
