from .core import BusBase

class Bus(BusBase):

    def pub_check_email(self, user):
        message = f"Enviado un mensaje de prueba a {user.email}"
        self.insert(user, message)

    def pub_new_member(self, member):
        message = (
            f"Se ha dado de alta un nuevo socio: {member.full_name}"
            f" con número de socio {member.pk}"
            )
        self.insert(member, message)

