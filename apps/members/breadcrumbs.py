from apps.commons.breadcrumbs import BreadCrumb


def bc_members():
    return BreadCrumb("Miembros", 'member:homepage')


def bc_membership() -> BreadCrumb:
    return bc_members().step("Permanencia", 'member:homepage')


def bc_password_change() -> BreadCrumb:
    return bc_members().step(
        "Cambiar contraseña",
        'member:password_change',
        )


def bc_address_change() -> BreadCrumb:
    return bc_members().step(
        "Cambiar dirección",
        'member:address_change',
        )

