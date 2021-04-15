class InvalidUsageError(Exception):
    status_code = 404

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        error_info = dict(self.payload or ())
        error_info['message'] = self.message
        return error_info


class NoHTMLElementFoundError(Exception):

    def __int__(self, message='Failed to scrape given element!'):
        super().__init__(message)
