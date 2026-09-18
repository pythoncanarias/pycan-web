from apps.commons.breadcrumbs import BreadCrumb

def bc_about():
    return BreadCrumb("Asociación Python Canarias", 'about:index')


def bc_us():
    return bc_about().step("Sobre la asociación", 'about:us')


def bc_join():
    return bc_about().step("Únete", 'about:join')


def bc_join_method():
    return bc_join().step("Procedimiento", 'about:join_method')


def bc_history():
    return bc_about().step("Historia", 'about:history')


def bc_allies():
    return bc_about().step("Aliados", 'about:allies')


def bc_faq():
    return bc_about().step("Preguntas frecuentes", 'about:faq')
