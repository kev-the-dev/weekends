#!/usr/bin/env python3
import unittest
import itertools
import random

'''
https://www.khanacademy.org/computing/computer-science/cryptography/modern-crypt/v/rsa-encryption-part-4

https://en.wikipedia.org/wiki/RSA_(cryptosystem)
'''

def hcfnaive(a,b): 
    '''
    gcd(a, b)
    '''
    if(b==0): 
        return a 
    else: 
        return hcfnaive(b,a%b) 


def lcm(a, b):
    return int(abs(a * b) / hcfnaive(a, b))


def phi_n(p1, p2):
    '''
    Computes Phi(N) where N is a private key in RSA
    using the prime numbers used to create N

    Phi(x) -> number of integers [1, x) which are not factors of x.

    Beacause Primes have no factors besides itself and 1, Phi(x: x is prime) -> x - 1

    Phi is multiplicitive e.g. Phi(x*y) = Phi(x) * Phi(y)

    So if N = p1 * p2, where p1 and p2 are primes
    Phi(N) = Phi(p1) * Phi(p2) = (p1 - 1) * (p2 -2)
    '''
    return lcm(p1 - 1, p2 - 1)


def encrypt_rsa(pub_key, msg):
    n, e = pub_key
    return (msg ** e) % n


def decrypt_rsa(priv_key, msg):
    d, n = priv_key
    return (msg ** d) % n


def d(phi_n, e):
    return int((2 * phi_n + 1) / e)

def odds(start, stop=None):
    return itertools.count(start, 2)

def primes():
    # 1 is prime
    yield 1
    # 3 is prime
    yield 3
    # Odd numbers >= 5 are prime
    # if they have no factors besides themselves and 1
    for n in odds(5):
        prime = True
        for i in range(3, n, 2):
            if n % i == 0:
                prime = False
                break
        if prime:
            yield n

BUNCH_OF_PRIMES = list(itertools.islice(primes(), 100))

def generate_e(phi_n):
    '''
    e is an odd number that does not share
    a factor with phi_n
    '''
    for i in BUNCH_OF_PRIMES[2:]:
        if phi_n % i != 0:
            return i



class RSAKeyPair(object):
    def __init__(self, p1, p2):
        # RSA key is created from 2 prime numbers
        self.p1, self.p2 = p1, p2

        self.n = self.p1 * self.p2
        self.phi_n = phi_n(self.p1, self.p2) 

        self.e = generate_e(self.phi_n)
        self.d = d(self.phi_n, self.e)

    @classmethod
    def Random(cls):
        p1, p2 = random.sample(BUNCH_OF_PRIMES, 2)
        return cls(p1, p2)

    def public_key(self):
        return self.n, self.e

    def private_key(self):
        return self.d, self.n

    def decrypt_msg(self, encrypted_msg):
        return decrypt_rsa(self.private_key(), encrypted_msg)


class TestRSA(unittest.TestCase):
    def test_can_encrypt_and_decrypt(self):
        alice = RSAKeyPair.Random()
        print("Alice p1={p1} p2={p2} N={n} Phi(N)={phi_n} e={e} d={d}".format(
            p1=alice.p1, p2=alice.p2, n=alice.n, phi_n=alice.phi_n, e=alice.e,
            d=alice.d))
        alice_pub = alice.public_key()
        print("Alice Public Key = {}".format(alice.public_key()))
        print("Alice's Private Key = {}".format(alice.private_key()))

        msg = ord('A')
        print("Msg = {}".format(msg))
        encrypted_msg = encrypt_rsa(alice_pub, msg)
        print("Encrypted Msg = {}".format(encrypted_msg))

        decrypted_msg = alice.decrypt_msg(encrypted_msg)
        print("Decrypted Msg = {}".format(decrypted_msg))

        self.assertEqual(msg, decrypted_msg)


if __name__ == '__main__':
    unittest.main()
