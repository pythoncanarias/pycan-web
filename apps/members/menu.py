from apps.commons.menu import Menu

main_menu = (
    Menu()
    .add_section('general', 'General')
    .add_menu_item("Perfil de usuario/a", "members:profile")
    .add_menu_item("Permanencia", "members:membership")
    .finished()
    .add_section('ops', 'Operaciones')
    .add_menu_item("Cambiar contraseña", "members:password_change")
    .add_menu_item("Salir (<i>Logout</i>)", "members:logout")
    .finished()
)
