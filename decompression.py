def decode_huffman(encoded_text, codes):
    if not encoded_text or not codes:
        raise ValueError("Encoded text or codes cannot be empty for decompression.")

    reverse_codes = {v: k for k, v in codes.items()}
    current_code = ""
    decoded_text = []

    print("Starting decompression...")
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codes:
            decoded_text.append(reverse_codes[current_code])
            print(f"Decoded character: {reverse_codes[current_code]}")
            current_code = ""

    if current_code:
        raise ValueError("Incomplete decoding. Remaining bits could not be decoded.")

    print("Decompression completed successfully.")
    return ''.join(decoded_text)
