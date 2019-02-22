from lib.exception.Option import OptionRequired


class ExploitOption:
    name = None
    required = False
    description = None
    value = None

    def __init__(self, name=None, required=False, description=None, value=None):
        self.name = name
        self.required = required
        self.description = description
        self.value = value

    def validate_option(self):
        if self.required and self.value is None:
            raise OptionRequired(self)

