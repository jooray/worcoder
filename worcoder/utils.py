from typing import List

# 10 bits per word for base-1024
RADIX_BITS = 10

class ChecksumError(Exception):
    pass

def bits_to_words_count(num_bits: int) -> int:
    """
    Round up to multiples of 10 bits for how many words needed.
    """
    return (num_bits + RADIX_BITS - 1) // RADIX_BITS

def int_to_base1024(value: int, length: int) -> List[int]:
    """
    Convert integer 'value' into big-endian base-1024 with exactly 'length' words.
    """
    out = []
    for _ in range(length):
        out.append(value & 0x3FF)  # 0x3FF = 1023
        value >>= 10
    return list(reversed(out))

def base1024_to_int(words: List[int]) -> int:
    """
    Combine base-1024 words [w1, w2, ...] in big-endian order into one integer.
    """
    val = 0
    for w in words:
        val = (val << 10) | w
    return val
