class MyException(Exception):
    def __init__(self, desc):
        self.desc = desc

    def __str__(self, ):
        return repr(self.desc)


class ConfException(MyException):
    pass

# Raised when Elasticsearch related class init failed (normally caused by incorrect config format)
class ElasticsearchInitException(MyException):
    pass

# Raised when some unexpected error happened on ES
# For example, can't find the index when we try to create or update an item
class ElasticsearchStateException(MyException):
    pass

class FileNotFound(Exception):
    def __init__(self, ):
        pass

    def __str__(self):
        return 'file not found'
