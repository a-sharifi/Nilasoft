class AutoScope:
    def __init__(self, object_name: str, service_name: str = "pds"):
        self.object_name = object_name.lower()
        self.service_name = service_name.lower()
        self.create = f"{self.service_name}:{self.object_name}:create"
        self.update = f"{self.service_name}:{self.object_name}:update"
        self.delete = f"{self.service_name}:{self.object_name}:delete"
        self.list = f"{self.service_name}:{self.object_name}:list"
        self.detail = f"{self.service_name}:{self.object_name}:get"

    def custom(self, action: str) -> str:
        return f"{self.service_name}:{self.object_name}:{action}"
