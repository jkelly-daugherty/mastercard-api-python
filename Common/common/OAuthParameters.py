import base64
import hashlib
import math
import random
import time
import common.oauthconstants

NONCE_LENGTH = 8
VALID_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

class OAuthParameters(object):

    def __init__(self, consumer_key):
        self.consumer_key = consumer_key
        self.timestamp = self.generate_timestamp()
        self.nonce = self.generate_nonce()
        self.signature_method = 'RSA-SHA1'
        self.oauth_version = '1.0'
        self.body_hash = ''
        self.signature = ''

    @staticmethod
    def generate_timestamp():
        return math.floor(time.time())

    @staticmethod
    def generate_nonce():
        rng = random.SystemRandom()
        ret_nonce = ''
        for idx in range(NONCE_LENGTH):
            ridx = rng.randint(0, len(VALID_CHARS) -1)
            ret_nonce = ret_nonce + VALID_CHARS[ridx]
        return ret_nonce

    def generate_body_hash(self,body):
        if body:
            self.body_hash = base64.b64encode(hashlib.sha1(body.encode('utf-8')).digest()).decode('utf-8')
        return self.body_hash

    def generate_parameters_hash(self):
        param_hash = {}
        param_hash[common.oauthconstants.OAUTH_CONSUMER_KEY] = self.consumer_key
        param_hash[common.oauthconstants.OAUTH_TIMESTAMP] = self.timestamp
        param_hash[common.oauthconstants.OAUTH_NONCE] = self.nonce
        param_hash[common.oauthconstants.OAUTH_SIGNATURE_METHOD] = self.signature_method
        param_hash[common.oauthconstants.OAUTH_VERSION] = self.oauth_version
        if len(self.body_hash) > 0:
            param_hash[common.oauthconstants.OAUTH_BODY_HASH] = self.body_hash
        return param_hash

    def print(self):
        print('OAuth Consumer Key: ' + self.consumer_key)
        print('OAuth Timestamp: ' + str(self.timestamp))
        print('OAuth Nonce: ' + self.nonce)
        print('Body Hash: ' + self.body_hash)
        print('OAuth Sig Method: ' + self.signature_method)
        print('OAuth Signature: ' + self.signature)
        print('OAuth Version: ' + self.oauth_version)






