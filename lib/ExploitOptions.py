from lib.exception.Option import OptionRequired


class ExploitOptions:
    options = None

    def __init__(self):
        self.options = []

    def add_option(self, option):
        self.options.append(option)

    def get_options(self):
        return self.options

    def get_option(self, name):
        for option in self.options:
            if option.name == name:
                return option.value
        return None

    def set_option(self, name, value):
        for idx, option in enumerate(self.options):
            if option.name == name:
                option.value = value
                self.options[idx] = option

    def validate(self):
        error = []
        for option in self.get_options():
            try:
                option.validate_option()
            except OptionRequired as e:
                error.append(e)
        if error:
            return [False, error]
        else:
            return [True, None]
