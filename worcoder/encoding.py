from typing import List

from .wordlist import words_from_indices, indices_from_words
from .rs1024 import create_checksum, verify_checksum, CHECKSUM_LENGTH_WORDS
from .utils import (
    ChecksumError,
    RADIX_BITS,
    bits_to_words_count,
    int_to_base1024,
    base1024_to_int,
)

# We'll pick a short customization string: b"str-data"
# Convert each byte into one 10-bit word (simple approach).
CUSTOMIZATION_INDICES = []

__all__ = [
    "str_to_words",
    "words_to_str",
    "str_to_mnemonic",
    "mnemonic_to_str",
]

def str_to_words(data: str, ascii_only: bool = False) -> List[str]:
    """
    Convert the given string into a list of mnemonic words, with a 3-word checksum appended.

    If ascii_only is True, optimizes encoding for ASCII-only strings (letters, numbers, basic punctuation).
    """
    if ascii_only:
        # Verify that all characters are ASCII
        try:
            data_bytes = data.encode("ascii")
        except UnicodeEncodeError:
            raise ValueError("ascii_only=True but data contains non-ASCII characters.")

        # Each character is represented with 7 bits
        bit_length = len(data) * 7

        # Convert the string into a bitstream
        val_int = 0
        for char in data:
            val_int = (val_int << 7) | ord(char)

        # Calculate how many 10-bit words needed for the data
        data_words_count = bits_to_words_count(bit_length)

        # Convert integer to base-1024 words
        data_indices = int_to_base1024(val_int, data_words_count)

    else:
        # Encode the data as UTF-8
        data_bytes = data.encode("utf-8")

        # Convert data bytes to a big integer
        val_int = int.from_bytes(data_bytes, byteorder="big")

        # Calculate how many 10-bit words needed for the data
        data_bits = len(data_bytes) * 8
        data_words_count = bits_to_words_count(data_bits)

        # Convert integer to base-1024 words
        data_indices = int_to_base1024(val_int, data_words_count)

    # Create the 3-word checksum
    csum = create_checksum(data_indices, CUSTOMIZATION_INDICES)

    # Combine data indices + checksum
    full_indices = data_indices + csum

    # Convert to actual word strings
    return words_from_indices(full_indices)

def words_to_str(words: List[str], ascii_only: bool = False) -> str:
    """
    Convert a list of mnemonic words (with 3-word checksum) back into the original string.
    Raises ChecksumError if the checksum is invalid.

    If ascii_only is True, expects the words to be encoded with ASCII compression.
    """
    # Convert words to base-1024 indices
    all_indices = indices_from_words(words)

    if len(all_indices) < CHECKSUM_LENGTH_WORDS:
        raise ChecksumError("Not enough words to contain data + checksum.")

    data_indices = all_indices[:-CHECKSUM_LENGTH_WORDS]
    checksum_part = all_indices[-CHECKSUM_LENGTH_WORDS:]

    # Verify checksum
    if not verify_checksum(data_indices + checksum_part, CUSTOMIZATION_INDICES):
        raise ChecksumError("Invalid mnemonic checksum.")

    if ascii_only:
        # Convert base-1024 data portion -> int
        val_int = base1024_to_int(data_indices)

        # Extract 7 bits per character
        bit_length = len(data_indices) * RADIX_BITS
        total_chars = bit_length // 7
        remaining_bits = bit_length % 7
        if remaining_bits != 0:
            # There are extra bits that should be zero
            if (val_int & ((1 << remaining_bits) - 1)) != 0:
                raise ChecksumError("Invalid encoding: extra bits detected.")
            val_int >>= remaining_bits

        # Extract characters
        chars = []
        for _ in range(total_chars):
            char_code = val_int & 0x7F  # 7 bits
            chars.append(chr(char_code))
            val_int >>= 7
        chars.reverse()
        return ''.join(chars)

    else:
        # Convert base-1024 data portion -> int -> bytes
        val_int = base1024_to_int(data_indices)
        # Calculate number of bytes
        data_bits = len(data_indices) * RADIX_BITS
        byte_length = (data_bits + 7) // 8
        raw_bytes = val_int.to_bytes(byte_length, "big")

        # Decode as UTF-8
        return raw_bytes.decode("utf-8", errors="replace")

def str_to_mnemonic(data: str, ascii_only: bool = False) -> str:
    """
    Convert the given string into a single mnemonic string (space-separated words).

    If ascii_only is True, optimizes encoding for ASCII-only strings.
    """
    word_list = str_to_words(data, ascii_only=ascii_only)
    return " ".join(word_list)

def mnemonic_to_str(mnemonic: str, ascii_only: bool = False) -> str:
    """
    Convert a space-separated mnemonic string back into the original data string.

    If ascii_only is True, expects the mnemonic to be encoded with ASCII compression.
    """
    words = mnemonic.strip().split()
    return words_to_str(words, ascii_only=ascii_only)
