class mod:
    def __init__(self, mod_name, mod_version,
                 mc_version, client_side, server_side, 
                 mod_loader, url, author) -> None:
        self.mod_name = mod_name
        self.mod_version = mod_version
        self.mc_version = mc_version
        self.client_side = client_side
        self.server_side = server_side
        self.mod_loader = mod_loader
        self.url = url
        self.author = author
