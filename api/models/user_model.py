from dataclasses import dataclass

@dataclass
class UserModel:
    email: str
    password: str

    def to_dict(self):
        return {"email": self.email, "password": self.password}
