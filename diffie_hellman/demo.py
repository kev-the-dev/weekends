#!/usr/bin/env python3
import random

'''
Prime numbers are magic!
'''

class DiffieHellman(object):
    def __init__(self, prime=23, base=5):
        self.prime = prime
        self.base = base

    def compute_pub_key(self, priv_key):
        return (self.base ** priv_key) % self.prime

    def compute_shared_key(self, my_priv_key, their_pub_key):
        return (their_pub_key ** my_priv_key) % self.prime


def main():
    df = DiffieHellman()

    alice_priv = random.randint(1, 100)
    print("Alice Private Key = {}".format(alice_priv))
    bob_priv = random.randint(1, 100)
    print("Bob Private Key = {}".format(bob_priv))

    print()
    alice_pub = df.compute_pub_key(alice_priv)
    print("Alice Public Key {}".format(alice_pub))
    bob_pub = df.compute_pub_key(bob_priv)
    print("Bob Public Key {}".format(bob_pub))

    print()
    alice_shared = df.compute_shared_key(alice_priv, bob_pub)
    print("Alice's Computed Shared key {}".format(alice_shared))
    bob_shared = df.compute_shared_key(bob_priv, alice_pub) 
    print("Bob's Computed SharedKey {}".format(bob_shared))


if __name__ == '__main__':
    main()
