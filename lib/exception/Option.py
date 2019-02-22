class OptionRequired(Exception):
    option = None

    def __init__(self, option):
        self.option = option

    def __str__(self):
        return "Module option {name} is required".format(name=self.option.name)
