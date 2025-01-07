from typing import List, Dict
from .wordlist_data import WORDLIST

RADIX = len(WORDLIST)  # Should be 1024

# Build reverse lookup from word -> index
WORD_INDEX_MAP: Dict[str, int] = {w: i for i, w in enumerate(WORDLIST)}

def words_from_indices(indices: List[int]) -> List[str]:
    return [WORDLIST[i] for i in indices]

def indices_from_words(words: List[str]) -> List[int]:
    try:
        return [WORD_INDEX_MAP[w.lower()] for w in words]
    except KeyError as e:
        raise ValueError(f"Invalid mnemonic word: {e}")
