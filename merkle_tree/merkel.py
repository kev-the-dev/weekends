#!/usr/bin/env python3
import hashlib
import sys
import pathlib
import base64

CHUNK_SIZE_BYTES = 500

def merkle(f, start, stop):
    '''
    f: fd
    start: first byte to hash, index 0
    stop: one past last byte to hash
    '''
    global CHUNK_SIZE_BYTES

    size = stop - start + 1
    hasher = hashlib.sha256()
    if size < CHUNK_SIZE_BYTES:
        f.seek(start)
        chunk = f.read(size)
        print("Hashing file [{start}, {stop}]".format(start=start, stop=stop-1))
        hasher.update(chunk)
        return (hasher.digest(), None, None)
    else:
        split = int((start + stop) / 2)
        left = merkle(f, start, split)
        left_hash = left[0]
        right = merkle(f, split, stop)
        right_hash = right[0]
        print("Combining h([{s1}, {t1}]) and h([{s2}, {t2}])".format(
            s1=start, t1=split-1, s2=split, t2=stop-1))
        hasher.update(left_hash)
        hasher.update(right_hash)
        return (hasher.digest(), left, right)


def print_merkle(merkle, indentions):
    root, left, right = merkle
    printable_hash= base64.b16encode(root)
    print( (' ' * indentions) + root.hex())
    if left is not None:
        print_merkle(left, indentions + 1)
    if right is not None:
        print_merkle(right, indentions + 2)
 

if __name__ == "__main__":
    h = hashlib.sha256()
    filename = sys.argv[1] 
    stat = pathlib.Path(filename).stat()
    file_size_bytes = stat.st_size
    with open(filename, 'rb') as f:
        merk_tuple = merkle(f, 0, file_size_bytes)
        print_merkle(merk_tuple, 0)
