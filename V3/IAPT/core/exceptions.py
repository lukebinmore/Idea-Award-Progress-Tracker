class IAPTError(Exception):
    def __init__(self, message, error=None, **kwargs):
        super().__init__(message)
        self.message = message
        self.details = error

        self.error_data = {}
        for key, value in kwargs.items():
            self.error_data[key] = value

        print(self.error_data)
