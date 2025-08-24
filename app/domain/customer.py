class Customer:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    def get_formatted_name(self) -> str:
        return f"{self.name} <{self.email}>"