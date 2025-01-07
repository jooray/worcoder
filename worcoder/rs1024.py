from typing import List

CHECKSUM_LENGTH_WORDS = 3

# The polynomial mod function from SLIP-0039 or BIP-39's "polymod".
# Specifically adapted for base-1024.
def _polymod(values: List[int]) -> int:
    """
    Polynomial checksum over the input values.
    The generator is slightly different from bech32 but conceptually similar.
    """
    # This generator set is from slip-0039 / "rs1024".
    GEN = (
        0xE0E040,
        0x1C1C080,
        0x3838100,
        0x7070200,
        0xE0E0009,
        0x1C0C2412,
        0x38086C24,
        0x3090FC48,
        0x21B1F890,
        0x03F3F120,
    )
    chk = 1
    for v in values:
        top = chk >> 20
        chk = ((chk & 0xFFFFF) << 10) ^ v
        for i in range(10):
            if (top >> i) & 1:
                chk ^= GEN[i]
    return chk

def create_checksum(data: List[int], custom: List[int]) -> List[int]:
    """
    data: the base-1024 indices of the payload
    custom: the base-1024 indices for the customization string
    returns the 3-word checksum
    """
    values = custom + data + [0]*CHECKSUM_LENGTH_WORDS
    poly = _polymod(values) ^ 1
    # Extract 3 words of 10 bits each from poly
    return [(poly >> (10 * i)) & 1023 for i in reversed(range(CHECKSUM_LENGTH_WORDS))]

def verify_checksum(data: List[int], custom: List[int]) -> bool:
    """
    data: the entire base-1024 sequence, including the last 3 words as checksum
    custom: the base-1024 indices for the customization string
    returns True if the checksum is valid
    """
    return _polymod(custom + data) == 1
