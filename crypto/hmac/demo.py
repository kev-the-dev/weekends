#!/usr/bin/env python3
import hmac
import hashlib
import base64

'''
HMAC is a scheme for efficient message authentication
and integrity check with a symetric key.

The digest of HMAC cryptographicaly valid for only
the specific key AND message used to create it.

It's a kind of digital signature, albeit with
a symetric key (unlike RSA, for example)

Weaknesses:
    - Requires a symetric key (must exchange securely)
    - No protection from replay attack (sending the same message
      twice is still valid). Can counteract by incorporaitng
      a sequence number (see SRTP protocol for example)
'''


def get_hmac(key, msg):
    hmac_obj = hmac.new(key.encode(), msg=msg.encode(), digestmod=hashlib.sha256) 
    return hmac_obj.digest()


def validate_hmac(key, msg, digest):
    expected = get_hmac(key, msg)
    return hmac.compare_digest(expected, digest)

def pretty_digest(digest):
    '''
    Raw digest bytes to printable str
    '''
    return base64.b64encode(digest).decode()


def fudge(data):
    '''
    Modifies data slightly
    '''
    if type(data) == str:    
        return (data[0] + '0') + data[1:]
    elif type(data) == bytes:
        return int.to_bytes(data[0] + 1, 1, 'big') + data[1:]
    else:
        raise Exception("unimplemented")


def main():
    msg = "foo"
    key = "password"
    digest = get_hmac(key, msg)
    digest_pretty = pretty_digest(digest)

    print("--- Correct HMAC is Valid ---")
    print("H({}, {}) --> {}".format(key, msg, 
        digest_pretty))
    print("Valid({}, {}, {}) --> {}".format(key, msg, digest_pretty,
        validate_hmac(key, msg, digest)))

    print("--- Fudged Key is Invalid ---")
    modified_key = fudge(key)
    print("Valid({}, {}, {}) --> {}".format(modified_key, msg, digest_pretty,
        validate_hmac(modified_key, msg, digest)))

    print("--- Fudged Msg is Invalid ---")
    modified_msg = fudge(msg)
    print("Valid({}, {}, {}) --> {}".format(key, modified_msg, digest_pretty,
        validate_hmac(key, modified_msg, digest)))

    print("--- Fudged HMAC is Invalid ---")
    modified_digest = fudge(digest)
    modified_digest_pretty = pretty_digest(modified_digest)
    print("Valid({}, {}, {}) --> {}".format(key, msg, modified_digest_pretty,
        validate_hmac(key, msg, modified_digest)))


if __name__ == '__main__':
    main()
