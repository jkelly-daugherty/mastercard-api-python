import base64
import common
import html
import Crypto.Hash.SHA as SHA
import Crypto.Signature.PKCS1_v1_5 as SIGNATURE
import requests
import urllib.parse

AMP = '&'
OAUTH_START_STRING = 'OAuth '
ERROR_STATUS_BOUNDARY = 300

USER_AGENT = 'MC API OAuth Framework v1.0-Python'


class Connector(object):

    def __init__(self, consumer_key, private_key):
        self.consumer_key = consumer_key
        self.private_key = private_key
        self.signature_base_string = ''
        self.auth_header = ''

    def do_request(self, url, request_method, body='', oauth_params=None):
        if not oauth_params:
            oauth_params = common.oauthparameters.OAuthParameters(self.consumer_key)

        if len(body) > 0:
            oauth_params.generate_body_hash(body)

        self.signature_base_string = self.generate_signature_base_string(url, request_method, oauth_params)
        self.signature_base_string = self.signature_base_string.replace('+', '%2520')
        self.sign(oauth_params)
        self.auth_header = self.build_auth_header_string(oauth_params)

        return self.connect(url, request_method, body)

    def generate_signature_base_string(self, url, request_method, oauth_params):
        return urllib.parse.quote_plus(request_method.upper()) + AMP + \
            urllib.parse.quote_plus(self.normalize_url(url)) + AMP + \
            urllib.parse.quote_plus(self.normalize_parameters(url, oauth_params))

    @staticmethod
    def normalize_url(url):
        tmp = url
        idx = tmp.find('?')
        # strip query string
        if idx > -1:
            tmp = tmp[0:idx]
        # strip port
        if tmp.rfind(':') > 5:
            tmp = tmp[0:tmp.rfind(':')]
        return tmp

    @staticmethod
    def normalize_parameters(url, oauth_parms):
        q_string_dict = urllib.parse.parse_qs(url[url.rfind('?') + 1:])
        o_auth_dict = oauth_parms.generate_parameters_hash()
        name_arr = []
        for key in q_string_dict:
            name_arr.append(key)
        for key in o_auth_dict:
            name_arr.append(key)
        name_arr.sort()
        parm = ''
        delim = ''
        for idx in range(len(name_arr)):
            if name_arr[idx] in q_string_dict:
                parm = parm + delim + name_arr[idx] + '=' + str(q_string_dict[name_arr[idx]][0])
            else:
                parm = parm + delim + name_arr[idx] + '=' + str(o_auth_dict[name_arr[idx]])
            delim = AMP
        return parm

    def sign(self, oauth_params):
        signer = SIGNATURE.new(self.private_key)
        digest = SHA.new(self.signature_base_string.encode('utf-8'))
        sign = signer.sign(digest)
        oauth_params.signature = urllib.parse.quote_plus(base64.b64encode(sign).decode('utf-8'))
        oauth_params.signature = oauth_params.signature.replace('+', '%20')
        oauth_params.signature = oauth_params.signature.replace('*', '%2A')
        oauth_params.signature = oauth_params.signature.replace('~', '%7E')

        oauth_params.print()

    @staticmethod
    def build_auth_header_string(oauth_params):
        header = ''
        header = header + common.oauthconstants.OAUTH_CONSUMER_KEY + '="' + oauth_params.consumer_key + '",'
        header = header + common.oauthconstants.OAUTH_NONCE + '="' + oauth_params.nonce + '",'
        header = header + common.oauthconstants.OAUTH_SIGNATURE + '="' + oauth_params.signature + '",'
        header = header + common.oauthconstants.OAUTH_SIGNATURE_METHOD + '="' + oauth_params.signature_method + '",'
        header = header + common.oauthconstants.OAUTH_TIMESTAMP + '="' + str(oauth_params.timestamp) + '",'
        header = header + common.oauthconstants.OAUTH_VERSION + '="' + oauth_params.oauth_version + '"'

        if len(oauth_params.body_hash) > 0:
            header = OAUTH_START_STRING + common.oauthconstants.OAUTH_BODY_HASH + '="' + \
                oauth_params.body_hash + '",' + header
        else:
            header = OAUTH_START_STRING + header

        print("\nHEADER: " + header)
        return header

    def connect(self, url, request_method, body=''):

        # All requests in API have ?Format=XML
        tmp_url = url[: url.rfind('?')]
        q_string_dict = urllib.parse.parse_qs(url[url.rfind('?') + 1:])

        if request_method.upper() == 'GET':
            response = requests.get(tmp_url, params=q_string_dict, headers=self.get_headers(), cert='./SSLCerts/EnTrust/cacert.pem')
        elif request_method.upper() == 'POST':
            response = requests.post(tmp_url, body, params=q_string_dict, headers=self.get_headers(body), cert='./SSLCerts/EnTrust/cacert.pem')
        elif request_method.upper() == 'PUT':
            response = requests.put(tmp_url, body, params=q_string_dict, headers=self.get_headers(body), cert='./SSLCerts/EnTrust/cacert.pem')
        elif request_method.upper() == 'DELETE':
            response = requests.delete(tmp_url, data=body, params=q_string_dict, headers=self.get_headers(body), cert='./SSLCerts/EnTrust/cacert.pem')
        else:
            raise ValueError('Unsupported HTTP Method')

        return self.check_response(response)

    def get_headers(self, body=''):
        if len(body) > 0:
            return {
                'Authorization': self.auth_header,
                'User-Agent': USER_AGENT,
                'content-type': 'application/xml;charset=UTF-8',
                'content-length': str(len(body))
            }
        else:
            return {
                'Authorization': self.auth_header,
                'User-Agent': USER_AGENT
            }

    @staticmethod
    def check_response(response):
        if response.status_code > ERROR_STATUS_BOUNDARY:
            tmp = response.content.decode('utf-8')
            if tmp.find('<Errors>') > 0:
                raise tmp
        return response.content.decode('utf-8')