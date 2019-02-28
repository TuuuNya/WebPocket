from lib.cmd2 import Cmd, with_category
from art import text2art, art
from utils.module import name_convert
from pathlib import Path
from colorama import Fore, Style
from tabulate import tabulate
from importlib import import_module, reload
from lib.Database import Database
from lib.ExploitOption import ExploitOption
from lib.exception.Module import ModuleNotUseException


class Pocket(Cmd, Database):
    colors = "Always"

    console_prompt = "{COLOR_START}WebPocket{COLOR_END}".format(COLOR_START="\033[4m", COLOR_END="\033[0m")
    console_prompt_end = " > "
    module_name = None
    module_class = None
    module_instance = None

    # command categories
    CMD_CORE = "Core Command"
    CMD_MODULE = "Module Command"

    def __init__(self):
        super(Pocket, self).__init__()
        Database.__init__(self)
        self.prompt = self.console_prompt + self.console_prompt_end
        self.hidden_commands.extend(['alias', 'edit', 'macro', 'py', 'pyscript', 'shell', 'shortcuts', 'load'])
        self.do_banner(None)

    @with_category(CMD_CORE)
    def do_banner(self, args):
        ascii_text = text2art("WebPocket", "rand")
        self.poutput("\n\n")
        self.poutput(ascii_text, '\n\n', color=Fore.LIGHTCYAN_EX)
        self.poutput("{art} WebPocket has {count} modules".format(art=art("inlove"), count=self.get_module_count()), "\n\n", color=Fore.MAGENTA)

    @with_category(CMD_MODULE)
    def do_list(self, args):
        modules = self.get_modules()
        self._print_modules(modules, "Module List:")
        self._print_item("The list is only retrieved from the database")
        self._print_item("If you add some new modules, please execute `db_rebuild` first\n\n")

    @with_category(CMD_MODULE)
    def do_search(self, args):
        search_conditions = args.split(" ")
        db_conditions = {}
        for condition in search_conditions:
            cd = condition.split("=")
            if len(cd) is 1:
                [module_name] = cd
                db_conditions['module_name'] = module_name
            else:
                [field, value] = cd
                if field in self.searchable_fields:
                    db_conditions[field] = value

        modules = self.search_modules(db_conditions)

        self._print_modules(modules, 'Search results:')
        self._print_item("The search is only retrieved from the database")
        self._print_item("If you add some new modules, please execute `db_rebuild` first\n\n")

    def complete_set(self, text, line, begidx, endidx):
        if len(line.split(" ")) > 2:
            completion_items = []
        else:
            completion_items = ['debug']
            if self.module_instance:
                completion_items += [option.name for option in self.module_instance.options.get_options()]
        return self.basic_complete(text, line, begidx, endidx, completion_items)

    @with_category(CMD_MODULE)
    def do_set(self, args):
        [arg, value] = args.split(" ")
        if arg == 'debug':
            self.debug = value
            return None

        if not self.module_instance:
            raise ModuleNotUseException()

        self.module_instance.options.set_option(arg, value)

    def complete_use(self, text, line, begidx, endidx):
        modules = [module[0] for module in self.get_modules()]
        return self.basic_complete(text, line, begidx, endidx, modules)

    @with_category(CMD_MODULE)
    def do_use(self, module_name, module_reload=False):
        module_file = name_convert(module_name)
        module_type = module_name.split("/")[0]

        if Path(module_file).is_file():
            self.module_name = module_name
            if module_reload:
                self.module_class = reload(self.module_class)
            else:
                self.module_class = import_module("modules.{module_name}".format(module_name=module_name.replace("/", ".")))
            self.module_instance = self.module_class.Exploit()
            self.set_prompt(module_type=module_type, module_name=module_name)
        else:
            self.poutput("Module/Exploit not found.")

    @with_category(CMD_MODULE)
    def do_back(self, args):
        self.module_name = None
        self.module_instance = None
        self.prompt = self.console_prompt + self.console_prompt_end

    @with_category(CMD_MODULE)
    def do_show(self, content):
        if not self.module_instance:
            raise ModuleNotUseException()

        if content == "info":
            info = self.module_instance.get_info()
            info_table = []
            self.poutput("Module info:", "\n\n", color=Fore.CYAN)
            for item in info.keys():
                info_table.append([item + ":", info.get(item)])
            self.poutput(tabulate(info_table, colalign=("right",), tablefmt="plain"), "\n\n")

        if content == "options" or content == "info":
            options = self.module_instance.options.get_options()
            default_options_instance = ExploitOption()
            options_table = []
            for option in options:
                options_table_row = []
                for field in default_options_instance.__dict__.keys():
                    options_table_row.append(getattr(option, field))
                options_table.append(options_table_row)

            self.poutput("Module options:", "\n\n", color=Fore.CYAN)
            self.poutput(
                tabulate(
                    options_table,
                    headers=default_options_instance.__dict__.keys(),
                ),
                "\n\n"
            )

        if content == "missing":
            missing_options = self.module_instance.get_missing_options()
            if len(missing_options) is 0:
                self.poutput("No option missing!", color=Fore.CYAN)
                return None

            default_options_instance = ExploitOption()
            missing_options_table = []
            for option in missing_options:
                options_table_row = []
                for field in default_options_instance.__dict__.keys():
                    options_table_row.append(getattr(option, field))
                missing_options_table.append(options_table_row)
            self.poutput("Missing Module options:", "\n\n", color=Fore.CYAN)
            self.poutput(
                tabulate(
                    missing_options_table,
                    headers=default_options_instance.__dict__.keys(),
                ),
                "\n\n"
            )

    @with_category(CMD_MODULE)
    def do_run(self, args):
        self.do_exploit(args=args)

    @with_category(CMD_MODULE)
    def do_exploit(self, args):
        if not self.module_instance:
            raise ModuleNotUseException()

        exploit_result = self.module_instance.exploit()
        if exploit_result.status:
            self._print_item("Exploit success!")
            self._print_item(exploit_result.success_message)
        else:
            self._print_item("Exploit failure!", color=Fore.RED)
            self._print_item(exploit_result.error_message, color=Fore.RED)
        self.poutput("{style}[*]{style_end} module execution completed".format(
            style=Fore.BLUE + Style.BRIGHT,
            style_end=Style.RESET_ALL
        ))

    @with_category(CMD_MODULE)
    def do_check(self, args):
        if not self.module_instance:
            raise ModuleNotUseException()

        exploit_result = self.module_instance.check()

        if exploit_result is None:
            self._print_item("Check Error: maybe this module does not support check or check function is valid")
            return None

        if exploit_result.status:
            self._print_item("Check success!")
            self._print_item(exploit_result.success_message)
        else:
            self._print_item("Exploit failure!", color=Fore.RED)
            self._print_item(exploit_result.error_message, color=Fore.RED)
        self.poutput("{style}[*]{style_end} module execution completed".format(
            style=Fore.BLUE + Style.BRIGHT,
            style_end=Style.RESET_ALL
        ))

    @with_category(CMD_CORE)
    def do_db_rebuild(self, args):
        self.db_rebuild()
        self.poutput("Database rebuild done.", color=Fore.GREEN)

    @with_category(CMD_MODULE)
    def do_reload(self, args):
        self.do_use(self.module_name, module_reload=True)

    def set_prompt(self, module_type, module_name):
        module_prompt = " {module_type}({color}{module_name}{color_end})".format(
            module_type=module_type,
            module_name=module_name.replace(module_type + "/", ""),
            color=Fore.RED,
            color_end=Fore.RESET
        )
        self.prompt = self.console_prompt + module_prompt + self.console_prompt_end

    def _print_modules(self, modules, title):
        self.poutput(title, "\n\n", color=Fore.CYAN)
        self.poutput(tabulate(modules, headers=('module_name', 'check', 'disclosure_date', 'description')), '\n\n')

    def _print_item(self, message, color=Fore.YELLOW):
        self.poutput("{style}[+]{style_end} {message}".format(
            style=color + Style.BRIGHT,
            style_end=Style.RESET_ALL,
            message=message,
        ))
