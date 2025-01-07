# worcoder

A simple library for converting an arbitrary string into a sequence of mnemonic words
and back, with an RS1024 checksum appended to detect errors.

JavaScript version: [worcoder-js](https://github.com/jooray/worcoder-js)
Progressive Web App: [deployed](https://cypherpunk.today/theworcoder/index.html), source:[theworcoder-pwa](https://github.com/jooray/theworcoder-pwa)

## Overview

This library takes a string (ASCII or UTF-8) and encodes it to base-1024 words
(based on SLIP-0039 wordlist). It then appends a three-word checksum
to the result. During decoding, the checksum is verified. If the checksum is invalid,
an exception is raised.

### Enhanced Encoding Options

To optimize encoding for pure ASCII strings (consisting only of letters, numbers, and basic punctuation),
the library provides an option to compress using ASCII-only characters. This reduces the number of bits
used per character, resulting in fewer words for ASCII-only data.

## Installation

First, ensure [Poetry](https://python-poetry.org/) is installed. Then clone or copy
this repository. In the project directory, run:

```bash
poetry install
```

This will install the library into Poetry's virtual environment.

## Usage

Once installed, you can do:

```python
from worcoder.encoding import (
    str_to_words,
    words_to_str,
    str_to_mnemonic,
    mnemonic_to_str,
)

data = "Hello, World!"

# Convert string -> list of words (default encoding)
word_list = str_to_words(data)
print("word_list:", word_list)

# Convert list of words -> original string
restored = words_to_str(word_list)
print("restored:", restored)

# Convert string -> single mnemonic string
mnemonic_string = str_to_mnemonic(data)
print("mnemonic:", mnemonic_string)

# Convert single mnemonic string -> original string
restored_again = mnemonic_to_str(mnemonic_string)
print("restored_again:", restored_again)

# Convert ASCII-only string -> list of words with ASCII compression
ascii_data = "Hello, World!"
ascii_word_list = str_to_words(ascii_data, ascii_only=True)
print("ascii_word_list:", ascii_word_list)

# Convert list of words with ASCII compression -> original string
restored_ascii = words_to_str(ascii_word_list, ascii_only=True)
print("restored_ascii:", restored_ascii)

# Convert ASCII-only string -> single mnemonic string with ASCII compression
ascii_mnemonic = str_to_mnemonic(ascii_data, ascii_only=True)
print("ascii_mnemonic:", ascii_mnemonic)

# Convert single mnemonic string with ASCII compression -> original string
restored_ascii_again = mnemonic_to_str(ascii_mnemonic, ascii_only=True)
print("restored_ascii_again:", restored_ascii_again)
```

If you tamper with any word in the list or mnemonic, calling `words_to_str()` or
`mnemonic_to_str()` will raise `ChecksumError` to indicate an invalid checksum.

### CLI Usage

**Run** the CLI script. For example:

```bash
poetry run python -m worcoder.cli --encode Hello there
```

This will print (without an extra newline) the resulting **mnemonic**.

To **encode** an ASCII-only string with compression, use the `--ascii-only` flag:

```bash
poetry run python -m worcoder.cli --encode --ascii-only "Hello, World!"
```

To **decode**, use:

```bash
poetry run python -m worcoder.cli --decode beyond gray strategy fitness lunch grownup review together negative cause ordinary mustang nuclear cause tidy volume enlarge injury round texture mandate switch burden thunder
```

To **decode** a mnemonic encoded with ASCII compression, use the `--ascii-only` flag:

```bash
poetry run python -m worcoder.cli --decode --ascii-only "beyond gray strategy fitness lunch grownup review together negative cause ordinary mustang nuclear cause tidy volume enlarge injury round texture mandate switch burden thunder"
```

## API Reference

### `str_to_words(data: str, ascii_only: bool = False) -> List[str]`

Convert the given string into a list of mnemonic words, with a 3-word checksum appended.

- `data`: The input string to encode.
- `ascii_only`: If `True`, optimizes encoding for ASCII-only strings (letters, numbers, basic punctuation).
  Defaults to `False`.

### `words_to_str(words: List[str], ascii_only: bool = False) -> str`

Convert a list of mnemonic words (with 3-word checksum) back into the original string.

- `words`: The list of mnemonic words to decode.
- `ascii_only`: If `True`, expects the words to be encoded with ASCII compression.
  Defaults to `False`.

### `str_to_mnemonic(data: str, ascii_only: bool = False) -> str`

Convert the given string into a single mnemonic string (space-separated words).

- `data`: The input string to encode.
- `ascii_only`: If `True`, optimizes encoding for ASCII-only strings. Defaults to `False`.

### `mnemonic_to_str(mnemonic: str, ascii_only: bool = False) -> str`

Convert a space-separated mnemonic string back into the original data string.

- `mnemonic`: The mnemonic string to decode.
- `ascii_only`: If `True`, expects the mnemonic to be encoded with ASCII compression.
  Defaults to `False`.
