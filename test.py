from worcoder.encoding import (
    str_to_words,
    words_to_str,
    str_to_mnemonic,
    mnemonic_to_str,
)

data = "Hello world!"
mnemonic_str = str_to_mnemonic(data)
print("Mnemonic:", mnemonic_str)

decoded_data = mnemonic_to_str(mnemonic_str)
print("Decoded data:", decoded_data)
