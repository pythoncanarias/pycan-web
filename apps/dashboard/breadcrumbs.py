from apps.commons.breadcrumbs import BreadCrumb


def bc_dashboard():
    return BreadCrumb("Dashboard", 'dashboard:index')


def bc_new_member():
    return bc_dashboard().step(
        "Nuevo miembro",
        'dashboard:new_member',
        )

def bc_active_members():
    return bc_dashboard().step(
        "Miembros activos",
        'dashboard:active_members',
        )



