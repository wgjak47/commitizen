from commitizen import factory


class Info:
    """Show in depth explanation of your rules."""

    def __init__(self, config: dict):
        self.config: dict = config
        self.cz = factory.commiter_factory(self.config)

    def __call__(self, *args, **kwargs):
        self.cz.show_info()
