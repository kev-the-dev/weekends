#!/usr/bin/env python3
import numpy as np


def binary_repr(int_data):
    binary = ''
    for x in int_data:
        binary += np.binary_repr(x)
    return binary


def binary_len(data_range, n):
    bits_per_symbol =  np.ceil(np.log2(data_range))
    return n * bits_per_symbol


def random_with_probalilities(output_shape, probabilities):
    return np.random.choice(len(probabilities), output_shape, p=probabilities)


def huffman_bt(probabilities):
    return np.argsort(probabilities)[::-1]


def huffman_compress(bt, data):
    out = np.empty((0,0), dtype=np.uint8)
    for symbol in data:
        finds = np.nonzero(bt == symbol)
        if len(finds) < 1:
            raise Exception("symbol out of range of huffman")
        find = finds[0]
        out = np.append(out, np.array(find, dtype=np.uint8))
    return out


def huffman_decompress(bt, data):
    return bt[data]


if __name__ == '__main__':
    # Determinism
    np.random.seed(seed=1337)

    probabilities = [0.2, 0.4, 0.3, .1]
    print("Probabilities", probabilities)

    sampled_data = random_with_probalilities(100, probabilities)
    print("Sampled Data:", sampled_data)

    sampled_data_binary_size = binary_len(len(probabilities), len(sampled_data))
    print("sampled_data_binary_size", sampled_data_binary_size)

    bt = huffman_bt(probabilities)
    print("BT", bt)

    compressed = huffman_compress(bt, sampled_data)
    print("Compressed", compressed)

    compressed_binary = binary_repr(compressed)
    print("Compressed binary", compressed_binary)

    compressed_binary_size = len(compressed_binary)
    print("Compressed binary size", compressed_binary_size)

    proportion_compressed = sampled_data_binary_size / compressed_binary_size - 1.
    print("Compressed {:.2f}%".format(100. * proportion_compressed))

    decompressed = huffman_decompress(bt, compressed)
    print("Decompressed", decompressed)

    if not np.all(decompressed == sampled_data):
        raise Exception("did not match")