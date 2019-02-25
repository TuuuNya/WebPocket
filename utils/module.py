from utils.files import ROOT_PATH


def name_convert(name):
    if name.find(".py") is not -1:
        module_name = name.replace("modules/", "").replace(".py", "")
        return module_name
    else:
        full_name = "{ROOT}/modules/{MODULE}.py".format(ROOT=ROOT_PATH, MODULE=name)
        return full_name
