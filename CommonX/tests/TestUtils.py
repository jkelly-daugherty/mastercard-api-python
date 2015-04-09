from tests import testconstants
from Crypto.PublicKey import RSA


class TestUtils():
    def __init__(self, environment):
        self._environment = environment

    def get_private_key(self):
        if self._environment == "PRODUCTION":
            return RSA.importKey(open(testconstants.TestConstants.PRODUCTION_PRIVATE_KEY_PATH, 'r').read(),
                          testconstants.TestConstants.PRODUCTION_PRIVATE_KEY_PASSWORD)
        else:
            return RSA.importKey(open(testconstants.TestConstants.SANDBOX_PRIVATE_KEY_PATH, 'r').read(),
                          testconstants.TestConstants.SANDBOX_PRIVATE_KEY_PASSWORD)