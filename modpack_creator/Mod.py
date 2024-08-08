class mod:
    def __init__(self, mod_name, mod_version,
                 mc_version, platform, mod_loader,
                 url, author) -> None:
        self.mod_name = mod_name
        self.mod_version = mod_version
        self.mc_version = mc_version
        self.platform = platform
        self.mod_loader = mod_loader
        self.url = url
        self.author = author
