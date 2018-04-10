class IndexExceedError(Exception):
    def __init__(self, url):
        self.message = url


class SubjectBlockedError(Exception):
    def __init__(self, url):
        self.message = url

class ContentFormatError(Exception):
    def __init__(self, url):
        self.message = url
