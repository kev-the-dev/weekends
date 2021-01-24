#!/usr/bin/env python3
import numpy as np

# Inspired by https://www.khanacademy.org/computing/computer-science/informationtheory/moderninfotheory/v/information-entropy
# Just learning about compression. Its cool that it can be done in a few lines of numpy!


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
    '''
    ex: huffman_bt([0.2, 0.4, 0.3, .1]
         returns [1, 2, 0, 3]
         which represents binary decision tree
                       x
                      1 x
                       2  x
                         0 3
        Where true/1 leads you left, false/0 leads you right.
        When you end up on a leaf, that's the symbol.
    ''' 
    return np.argsort(probabilities)[::-1]


def huffman_compress(bt, data):
    out = np.empty((0,0), dtype=np.uint)
    for symbol in data:
        finds = np.nonzero(bt == symbol)
        if len(finds) < 1:
            raise Exception("symbol out of range of huffman")
        find = finds[0]
        out = np.append(out, np.array(find, dtype=np.uint))
    return out


def huffman_decompress(bt, data):
    return bt[data]


def entropy(probabilities):
    return -np.sum(np.multiply(probabilities, np.log2(probabilities)))


if __name__ == '__main__':
    # Determinism
    np.random.seed(seed=1390)

    # Define a discrete distibution [P(0), P(1), ...]
    probabilities = [0.2, 0.4, 0.3, .1]
    print("Probabilities", probabilities)

    # The "entropy" of the data. This is theoretical max compression ratio
    e = entropy(probabilities)
    print("Entropy", e)

    # Generate some random data from this distibution
    n = 100
    sampled_data = random_with_probalilities(n, probabilities)
    # print("Sampled Data:", sampled_data)

    # If this data was represented in binary, with the fewest possible bits
    # to represent a symbol, how big would it be?
    sampled_data_binary_size = binary_len(len(probabilities), len(sampled_data))
    print("sampled_data_binary_size", sampled_data_binary_size)

    # Assemble the huffman binary tree
    bt = huffman_bt(probabilities)
    # print("BT", bt)

    compressed = huffman_compress(bt, sampled_data)
    # print("Compressed", compressed)

    compressed_binary = binary_repr(compressed)
    # print("Compressed binary", compressed_binary)

    compressed_binary_size = len(compressed_binary)
    print("Compressed binary size", compressed_binary_size)

    compressed_ratio = sampled_data_binary_size / compressed_binary_size
    print("Compressed ratio", compressed_ratio)

    proportion_compressed = sampled_data_binary_size / compressed_binary_size - 1.
    print("Compressed {:.2f}%".format(100. * proportion_compressed))

    decompressed = huffman_decompress(bt, compressed)
    # print("Decompressed", decompressed)

    # Sanity check that we compressed and decompressed to the same data
    if not np.all(decompressed == sampled_data):
        raise Exception("did not match")