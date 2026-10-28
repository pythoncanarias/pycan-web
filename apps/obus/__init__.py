from .core import BusBase

class Bus(BusBase):

    def pub_check_email(self, user):
        message = f"Enviado un mensaje de prueba a {user.email}"
        self.insert(user, message)
