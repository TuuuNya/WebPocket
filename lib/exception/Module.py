class ModuleNotUseException(Exception):
    def __str__(self):
        return "Please use a module"
