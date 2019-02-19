class Module:
    name = None
    description = None
    disclosure_date = None
    REQUIRED_FIELDS = ['name', 'description']

    def update_info(self, info):
        self.name = info.name
        self.description = info.description
        self.disclosure_date = info.disclosure_date

    def register_options(self, option_name, option_required, option_description, option_default = None):
        setattr(self, option_name, option_default)
