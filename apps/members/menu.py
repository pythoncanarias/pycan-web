from apps.commons.menu import Menu

def main_menu(request):
    return (Menu(request)
        .add_section('general', 'General')
        .add_menu_item("Perfil de usuario/a", "members:homepage")
        .add_menu_item("Permanencia", "members:membership")
        .finished()
        .add_section('ops', 'Operaciones')
        .add_menu_item("Cambiar contraseña", "members:password_change")
        .add_menu_item("Cambiar dirección", "members:address_change")
        .add_menu_item("Salir (<i>Logout</i>)", "members:member_logout")
        .finished()
        )
