class ExploitResult:
    def __init__(self):
        self.status = False
        self.data = {}
        self.success_message = None
        self.error_message = None

    def success(self, message, data=None):
        self.status = True
        self.data = data
        self.success_message = message

    def failure(self, error_message):
        self.status = False
        self.error_message = error_message
