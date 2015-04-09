import urllib.parse

class UrlUtil(object):
    @staticmethod
    def add_query_parameter(url, descriptor, value):
        if value is not None and value is not '':
            url = url + '&' + descriptor + '=' + urllib.parse.quote_plus(str(value))
        return url