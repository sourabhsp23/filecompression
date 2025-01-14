import heapq
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        return f"HuffmanNode(char={self.char}, freq={self.freq})"

def calculate_frequency(text):
    frequency = defaultdict(int)
    for char in text:
        frequency[char] += 1
    return frequency

def build_huffman_tree(text):
    frequency = calculate_frequency(text)
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    if priority_queue:
        return priority_queue[0]
    return None

def build_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}
    if node is None:
        return codes

    if node.char is not None:
        codes[node.char] = current_code
        print(f"Character '{node.char}' has code: {current_code}")

    build_codes(node.left, current_code + "0", codes)
    build_codes(node.right, current_code + "1", codes)

    return codes

def huffman_compress(text):
    if not text:
        raise ValueError("Input text cannot be empty for compression.")

    tree = build_huffman_tree(text)
    if not tree:
        return "", {}

    codes = build_codes(tree)
    encoded_text = ''.join(codes[char] for char in text)
    
    print("Compression completed successfully.")
    print(f"Encoded text: {encoded_text[:100]}... (truncated for display)")

    return encoded_text, codes

def save_compressed(encoded_text, output_file):
    byte_array = int(encoded_text, 2).to_bytes((len(encoded_text) + 7) // 8, byteorder='big')
    with open(output_file, 'wb') as f:
        f.write(byte_array)
    print(f"Compressed data saved to {output_file}")
