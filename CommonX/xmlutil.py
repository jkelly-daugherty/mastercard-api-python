class XMLUtil():
    def verify_not_none(self, value):
        if value is None:
            return None
        else:
            return value.text